#!/usr/bin/env python3
"""Façade et point d'entrée stable de Sentinel 0.4.0."""

from cli import build_parser, main
from configuration import ConfigurationError, Settings, load_settings
from diagnostic import collect_status, render_status
from logging_support import JsonFormatter, configure_logging
from runtime import healthcheck, sd_notify, serve
from state import is_ready, read_status, write_status
from version import VERSION
from web import SentinelHandler, SentinelServer, create_server


# Ces imports forment une façade compatible pour les TP et les tests cumulés.
if __name__ == "__main__":
    raise SystemExit(main())
