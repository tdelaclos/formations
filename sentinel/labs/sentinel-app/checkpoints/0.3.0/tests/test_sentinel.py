"""Tests du checkpoint Sentinel 0.3.0."""

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


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "src" / "sentinel.py"
sys.path.insert(0, str(ROOT / "src"))
SPEC = importlib.util.spec_from_file_location("sentinel_app", PROGRAM)
assert SPEC is not None and SPEC.loader is not None
SENTINEL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SENTINEL
SPEC.loader.exec_module(SENTINEL)


class SentinelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.temporary.name)
        self.settings = SENTINEL.Settings(root / "state", "127.0.0.1", 0)
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

    def test_health(self) -> None:
        status, payload = self.fetch("/health")
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"status": "ok", "version": "0.3.0"})

    def test_persisted_status(self) -> None:
        status, payload = self.fetch("/api/v1/status")
        self.assertEqual(status, 200)
        self.assertEqual(payload["application"], "sentinel")

    def test_unknown_route_is_rejected(self) -> None:
        with self.assertRaises(urllib.error.HTTPError) as context:
            urllib.request.urlopen(self.base_url + "/admin", timeout=2)
        self.assertEqual(context.exception.code, 404)

    def test_configuration_rejects_invalid_port(self) -> None:
        root = pathlib.Path(self.temporary.name)
        config = root / "invalid.conf"
        config.write_text(
            "[server]\nlisten_address = 127.0.0.1\nlisten_port = 70000\n"
            "[storage]\nstate_directory = state\n",
            encoding="utf-8",
        )
        with self.assertRaises(SENTINEL.ConfigurationError):
            SENTINEL.load_settings(config)


if __name__ == "__main__":
    unittest.main()
