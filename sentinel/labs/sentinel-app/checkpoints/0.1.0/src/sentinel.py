#!/usr/bin/env python3
"""Première version exécutable de l'application pédagogique Sentinel."""

from __future__ import annotations

import argparse
import json
import platform
import socket
from collections.abc import Sequence


VERSION = "0.1.0"


def collect_status() -> dict[str, str]:
    """Retourne un diagnostic local court et sérialisable."""

    return {
        "application": "sentinel",
        "version": VERSION,
        "hostname": socket.gethostname(),
        "kernel": platform.release(),
        "python": platform.python_version(),
        "status": "ok",
    }


def render_status(status: dict[str, str], output_format: str) -> str:
    """Produit une sortie stable pour un humain ou un autre programme."""

    if output_format == "json":
        return json.dumps(status, ensure_ascii=False, sort_keys=True)

    order = ("application", "version", "hostname", "kernel", "python", "status")
    return "\n".join(f"{key}: {status[key]}" for key in order)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description="Diagnostic local du laboratoire Sentinel",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    commands = parser.add_subparsers(dest="command", required=True)
    status = commands.add_parser("status", help="afficher l'état local")
    status.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="format de la sortie",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "status":
        print(render_status(collect_status(), args.format))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
