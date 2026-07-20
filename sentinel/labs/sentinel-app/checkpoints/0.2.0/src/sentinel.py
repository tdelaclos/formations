#!/usr/bin/env python3
"""Sentinel 0.2.0 : diagnostic local, configuration et état persistant."""

from __future__ import annotations

import argparse
import configparser
import json
import os
import platform
import socket
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


VERSION = "0.2.0"


class ConfigurationError(ValueError):
    """Signale une configuration absente ou invalide."""


@dataclass(frozen=True)
class Settings:
    state_directory: Path

    @property
    def state_file(self) -> Path:
        return self.state_directory / "status.json"


def collect_status() -> dict[str, str]:
    return {
        "application": "sentinel",
        "version": VERSION,
        "hostname": socket.gethostname(),
        "kernel": platform.release(),
        "python": platform.python_version(),
        "status": "ok",
    }


def render_status(status: dict[str, str], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(status, ensure_ascii=False, sort_keys=True)

    order = ("application", "version", "hostname", "kernel", "python", "status")
    return "\n".join(f"{key}: {status[key]}" for key in order)


def load_settings(config_path: Path) -> Settings:
    parser = configparser.ConfigParser(interpolation=None)
    if not parser.read(config_path, encoding="utf-8"):
        raise ConfigurationError(f"configuration introuvable: {config_path}")

    if not parser.has_option("storage", "state_directory"):
        raise ConfigurationError("option requise: [storage] state_directory")

    configured = Path(parser.get("storage", "state_directory")).expanduser()
    if not configured.is_absolute():
        configured = config_path.resolve().parent / configured

    return Settings(state_directory=configured.resolve())


def write_status(settings: Settings, status: dict[str, str]) -> None:
    settings.state_directory.mkdir(mode=0o750, parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=settings.state_directory,
        prefix=".status-",
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o640)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(status, stream, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, settings.state_file)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def read_status(settings: Settings) -> dict[str, str]:
    try:
        with settings.state_file.open(encoding="utf-8") as stream:
            payload = json.load(stream)
    except FileNotFoundError as exc:
        raise RuntimeError("aucun état enregistré") from exc

    if not isinstance(payload, dict) or payload.get("application") != "sentinel":
        raise RuntimeError("état Sentinel invalide")
    return {str(key): str(value) for key, value in payload.items()}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sentinel")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/sentinel.conf"),
        help="chemin du fichier de configuration",
    )
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="valider la configuration puis quitter",
    )

    commands = parser.add_subparsers(dest="command")
    status = commands.add_parser("status", help="afficher le diagnostic courant")
    status.add_argument("--format", choices=("text", "json"), default="text")
    commands.add_parser("record", help="enregistrer le diagnostic courant")
    show = commands.add_parser("show", help="afficher le dernier état enregistré")
    show.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.check_config:
            load_settings(args.config)
            print(f"configuration valide: {args.config}")
            return 0

        if args.command == "status":
            print(render_status(collect_status(), args.format))
            return 0

        if args.command == "record":
            settings = load_settings(args.config)
            write_status(settings, collect_status())
            print(settings.state_file)
            return 0

        if args.command == "show":
            settings = load_settings(args.config)
            print(render_status(read_status(settings), args.format))
            return 0
    except (ConfigurationError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"sentinel: {exc}", file=sys.stderr)
        return 1

    build_parser().print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
