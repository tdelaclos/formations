"""CLI qui assemble stockage et serveur HTTP sans dupliquer leur logique."""

import argparse
import json
import logging
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Optional

from configuration import ConfigurationError, load_settings
from diagnostic import collect_status, render_status
from state import read_status, write_status
from version import VERSION
from web import create_server


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sentinel")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--config", type=Path, default=Path("config/sentinel.conf"))
    parser.add_argument("--check-config", action="store_true")
    commands = parser.add_subparsers(dest="command")
    status = commands.add_parser("status")
    status.add_argument("--format", choices=("text", "json"), default="text")
    commands.add_parser("record")
    show = commands.add_parser("show")
    show.add_argument("--format", choices=("text", "json"), default="text")
    commands.add_parser("serve")
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

        settings = load_settings(args.config)
        if args.command == "record":
            write_status(settings, collect_status())
            print(settings.state_file)
            return 0
        if args.command == "show":
            print(render_status(read_status(settings), args.format))
            return 0
        if args.command == "serve":
            write_status(settings, collect_status())
            logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
            with create_server(settings) as server:
                logging.info("écoute sur %s:%s", *server.server_address)
                server.serve_forever()
            return 0
    except (ConfigurationError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"sentinel: {exc}", file=sys.stderr)
        return 1

    build_parser().print_help(sys.stderr)
    return 2
