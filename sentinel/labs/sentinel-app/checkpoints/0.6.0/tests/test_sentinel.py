"""Tests du checkpoint Sentinel 0.6.0."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import shutil
import ssl
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from dataclasses import replace
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "src" / "sentinel.py"
sys.path.insert(0, str(ROOT / "src"))
import runtime as RUNTIME
SPEC = importlib.util.spec_from_file_location("sentinel_app", PROGRAM)
assert SPEC is not None and SPEC.loader is not None
SENTINEL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SENTINEL
SPEC.loader.exec_module(SENTINEL)


class SentinelTests(unittest.TestCase):
    def issue_certificate(
        self, root: pathlib.Path, name: str, ca_certificate: pathlib.Path, ca_key: pathlib.Path, usage: str
    ) -> tuple[pathlib.Path, pathlib.Path]:
        key = root / f"{name}.key"
        request = root / f"{name}.csr"
        certificate = root / f"{name}.crt"
        subprocess.run(
            [
                "openssl", "req", "-new", "-newkey", "rsa:2048", "-nodes",
                "-keyout", str(key), "-out", str(request), "-subj", f"/CN={name}",
                "-addext", f"subjectAltName=DNS:{name}",
                "-addext", f"extendedKeyUsage={usage}",
            ],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "openssl", "x509", "-req", "-in", str(request),
                "-CA", str(ca_certificate), "-CAkey", str(ca_key),
                "-CAcreateserial", "-out", str(certificate), "-days", "1",
                "-copy_extensions", "copy",
            ],
            check=True,
            capture_output=True,
        )
        return certificate, key

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.temporary.name)
        self.settings = SENTINEL.Settings(root / "state", "127.0.0.1", 0, "INFO")
        SENTINEL.write_status(self.settings, SENTINEL.collect_status())
        self.server = SENTINEL.create_server(self.settings)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temporary.cleanup()

    def fetch(self, path: str) -> tuple[int, dict[str, str]]:
        with urllib.request.urlopen(self.base_url + path, timeout=2) as response:
            return response.status, json.load(response)

    def test_health_and_readiness_are_distinct(self) -> None:
        health = self.fetch("/health")[1]
        self.assertEqual(health["status"], "ok")
        self.assertEqual(health["version"], "0.6.0")
        self.assertEqual(self.fetch("/ready")[1]["status"], "ready")

        self.settings.state_file.unlink()
        self.assertEqual(self.fetch("/health")[0], 200)
        with self.assertRaises(urllib.error.HTTPError) as context:
            urllib.request.urlopen(self.base_url + "/ready", timeout=2)
        self.assertEqual(context.exception.code, 503)

    def test_healthcheck_uses_readiness(self) -> None:
        runtime = SENTINEL.Settings(
            self.settings.state_directory,
            "127.0.0.1",
            self.server.server_port,
            "INFO",
        )
        self.assertTrue(SENTINEL.healthcheck(runtime))

    def test_sd_notify_sends_datagram(self) -> None:
        root = pathlib.Path(self.temporary.name)
        path = root / "notify.sock"
        with mock.patch.object(RUNTIME.socket, "socket") as socket_factory:
            notifier = socket_factory.return_value.__enter__.return_value
            self.assertTrue(SENTINEL.sd_notify("READY=1", {"NOTIFY_SOCKET": str(path)}))
            notifier.connect.assert_called_once_with(str(path))
            notifier.sendall.assert_called_once_with(b"READY=1")

    def test_invalid_log_level_is_rejected(self) -> None:
        root = pathlib.Path(self.temporary.name)
        config = root / "invalid.conf"
        config.write_text(
            "[server]\nlisten_address = 127.0.0.1\nlisten_port = 8443\n"
            "[storage]\nstate_directory = state\n[logging]\nlevel = VERBOSE\n",
            encoding="utf-8",
        )
        with self.assertRaises(SENTINEL.ConfigurationError):
            SENTINEL.load_settings(config)

    def test_tls_cannot_be_enabled_without_key_material(self) -> None:
        root = pathlib.Path(self.temporary.name)
        config = root / "missing-tls.conf"
        config.write_text(
            "[server]\nlisten_address = 127.0.0.1\nlisten_port = 8443\n"
            "[storage]\nstate_directory = state\n"
            "[tls]\nenabled = true\nrequire_client_certificate = true\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(SENTINEL.ConfigurationError, "TLS"):
            SENTINEL.load_settings(config)

    def test_only_configured_dns_san_is_authorized(self) -> None:
        certificate = {
            "subjectAltName": (
                ("DNS", "agent01.example.test"),
                ("IP Address", "192.0.2.10"),
            )
        }
        self.assertTrue(
            SENTINEL.is_authorized_certificate(
                certificate, ("agent01.example.test",)
            )
        )
        self.assertFalse(
            SENTINEL.is_authorized_certificate(
                certificate, ("agent02.example.test",)
            )
        )

    @unittest.skipUnless(shutil.which("openssl"), "openssl requis")
    def test_mtls_then_identity_authorization(self) -> None:
        root = pathlib.Path(self.temporary.name) / "pki"
        root.mkdir()
        ca_key = root / "ca.key"
        ca_certificate = root / "ca.crt"
        subprocess.run(
            [
                "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                "-keyout", str(ca_key), "-out", str(ca_certificate),
                "-subj", "/CN=Sentinel Test CA", "-days", "1",
                "-addext", "basicConstraints=critical,CA:TRUE",
            ],
            check=True,
            capture_output=True,
        )
        server_certificate, server_key = self.issue_certificate(
            root, "localhost", ca_certificate, ca_key, "serverAuth"
        )
        allowed_certificate, allowed_key = self.issue_certificate(
            root, "agent01.example.test", ca_certificate, ca_key, "clientAuth"
        )
        denied_certificate, denied_key = self.issue_certificate(
            root, "agent02.example.test", ca_certificate, ca_key, "clientAuth"
        )

        settings = SENTINEL.Settings(
            root / "state",
            "127.0.0.1",
            0,
            "INFO",
            True,
            server_certificate,
            server_key,
            ca_certificate,
            True,
            allowed_certificate,
            allowed_key,
            ("agent01.example.test",),
        )
        SENTINEL.write_status(settings, SENTINEL.collect_status())
        server = SENTINEL.create_server(settings)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = f"https://localhost:{server.server_port}/health"

        def client_context(certificate: pathlib.Path, key: pathlib.Path) -> ssl.SSLContext:
            context = ssl.create_default_context(cafile=ca_certificate)
            context.load_cert_chain(certificate, key)
            return context

        try:
            with urllib.request.urlopen(
                url,
                context=client_context(allowed_certificate, allowed_key),
                timeout=3,
            ) as response:
                self.assertEqual(response.status, 200)

            runtime = replace(
                settings,
                listen_port=server.server_port,
                healthcheck_server_name="localhost",
            )
            self.assertTrue(SENTINEL.healthcheck(runtime))

            with self.assertRaises(urllib.error.HTTPError) as denied:
                urllib.request.urlopen(
                    url,
                    context=client_context(denied_certificate, denied_key),
                    timeout=3,
                )
            self.assertEqual(denied.exception.code, 403)

            with self.assertRaises((urllib.error.URLError, ssl.SSLError)):
                urllib.request.urlopen(
                    url,
                    context=ssl.create_default_context(cafile=ca_certificate),
                    timeout=3,
                )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
