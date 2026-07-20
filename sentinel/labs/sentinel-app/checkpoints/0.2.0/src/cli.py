"""Interface en ligne de commande de Sentinel 0.2.0."""

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Optional

from configuration import ConfigurationError, load_settings
from diagnostic import collect_status, render_status
from state import read_status, write_status
from version import VERSION


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sentinel")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/sentinel.conf"),
        help="chemin du fichier de configuration",
    )
    parser.add_argument("--check-config", action="store_true")
    commands = parser.add_subparsers(dest="command")
    status = commands.add_parser("status")
    status.add_argument("--format", choices=("text", "json"), default="text")
    commands.add_parser("record")
    show = commands.add_parser("show")
    show.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Orchestre les modules sans contenir leur logique métier."""

    args = build_parser().parse_args(argv)
    try:
        if args.check_config:
            load_settings(args.config)
            print(f"configuration valide: {args.config}")
            return 0
        if args.command == "status":
            print(render_status(collect_status(), args.format))
            return 0

        settings = load_settings(args.config)
        if args.command == "record":
            write_status(settings, collect_status())
            print(settings.state_file)
            return 0
        if args.command == "show":
            print(render_status(read_status(settings), args.format))
            return 0
    except (ConfigurationError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"sentinel: {exc}", file=sys.stderr)
        return 1

    build_parser().print_help(sys.stderr)
    return 2
