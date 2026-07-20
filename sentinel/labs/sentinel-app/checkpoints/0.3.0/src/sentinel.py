#!/usr/bin/env python3
"""Façade et point d'entrée stable de Sentinel 0.3.0."""

from cli import build_parser, main
from configuration import ConfigurationError, Settings, load_settings
from diagnostic import collect_status, render_status
from state import read_status, write_status
from version import VERSION
from web import SentinelHandler, SentinelServer, create_server


# Les tests des versions précédentes peuvent garder la même API d'import.
__all__ = [
    "VERSION", "ConfigurationError", "Settings", "SentinelHandler",
    "SentinelServer", "build_parser", "collect_status", "create_server",
    "load_settings", "main", "read_status", "render_status", "write_status",
]


if __name__ == "__main__":
    raise SystemExit(main())
