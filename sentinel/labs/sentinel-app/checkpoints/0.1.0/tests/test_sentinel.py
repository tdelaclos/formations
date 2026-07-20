"""Tests du checkpoint Sentinel 0.1.0."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "src" / "sentinel.py"

SPEC = importlib.util.spec_from_file_location("sentinel_app", PROGRAM)
assert SPEC is not None and SPEC.loader is not None
SENTINEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SENTINEL)


class SentinelTests(unittest.TestCase):
    def test_status_contract(self) -> None:
        status = SENTINEL.collect_status()

        self.assertEqual(status["application"], "sentinel")
        self.assertEqual(status["version"], "0.1.0")
        self.assertEqual(status["status"], "ok")
        self.assertTrue(status["hostname"])
        self.assertTrue(status["kernel"])

    def test_json_is_machine_readable(self) -> None:
        payload = SENTINEL.render_status(SENTINEL.collect_status(), "json")

        self.assertEqual(json.loads(payload)["status"], "ok")

    def test_version_command(self) -> None:
        result = subprocess.run(
            [sys.executable, str(PROGRAM), "--version"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.stdout.strip(), "sentinel 0.1.0")

    def test_unknown_format_is_rejected(self) -> None:
        result = subprocess.run(
            [sys.executable, str(PROGRAM), "status", "--format", "xml"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
