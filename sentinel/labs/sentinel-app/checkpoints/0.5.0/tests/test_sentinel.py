"""Tests du checkpoint Sentinel 0.5.0."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "src" / "sentinel.py"
SPEC = importlib.util.spec_from_file_location("sentinel_app", PROGRAM)
assert SPEC is not None and SPEC.loader is not None
SENTINEL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SENTINEL
SPEC.loader.exec_module(SENTINEL)


class SentinelTests(unittest.TestCase):
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
        self.assertEqual(health["version"], "0.5.0")
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
        with mock.patch.object(SENTINEL.socket, "socket") as socket_factory:
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


if __name__ == "__main__":
    unittest.main()
