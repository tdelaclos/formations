"""Tests du checkpoint Sentinel 0.2.0."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import stat
import subprocess
import sys
import tempfile
import unittest
from typing import Optional


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "src" / "sentinel.py"
SPEC = importlib.util.spec_from_file_location("sentinel_app", PROGRAM)
assert SPEC is not None and SPEC.loader is not None
SENTINEL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SENTINEL
SPEC.loader.exec_module(SENTINEL)


class SentinelTests(unittest.TestCase):
    def create_config(self, root: pathlib.Path, content: Optional[str] = None) -> pathlib.Path:
        config = root / "sentinel.conf"
        config.write_text(content or "[storage]\nstate_directory = state\n", encoding="utf-8")
        return config

    def test_previous_status_contract_is_preserved(self) -> None:
        status = SENTINEL.collect_status()
        self.assertEqual(status["application"], "sentinel")
        self.assertEqual(status["status"], "ok")

    def test_relative_state_directory_is_relative_to_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            settings = SENTINEL.load_settings(self.create_config(root))
            self.assertEqual(settings.state_directory, root / "state")

    def test_atomic_state_has_restricted_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            settings = SENTINEL.load_settings(self.create_config(root))
            SENTINEL.write_status(settings, SENTINEL.collect_status())

            stored = SENTINEL.read_status(settings)
            mode = stat.S_IMODE(settings.state_file.stat().st_mode)
            self.assertEqual(stored["application"], "sentinel")
            self.assertEqual(mode, 0o640)
            self.assertEqual(list(settings.state_directory.glob(".status-*")), [])

    def test_invalid_configuration_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = self.create_config(pathlib.Path(directory), "[storage]\n")
            result = subprocess.run(
                [sys.executable, str(PROGRAM), "--config", str(config), "--check-config"],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("state_directory", result.stderr)

    def test_record_and_show_commands(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = self.create_config(pathlib.Path(directory))
            subprocess.run(
                [sys.executable, str(PROGRAM), "--config", str(config), "record"],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(PROGRAM),
                    "--config",
                    str(config),
                    "show",
                    "--format",
                    "json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(result.stdout)["status"], "ok")


if __name__ == "__main__":
    unittest.main()
