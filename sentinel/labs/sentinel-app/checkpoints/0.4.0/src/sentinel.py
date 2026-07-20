#!/usr/bin/env python3
"""Sentinel 0.4.0 : service HTTP exploitable par systemd."""

from __future__ import annotations

import argparse
import configparser
import json
import logging
import os
import platform
import signal
import socket
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


VERSION = "0.4.0"
LOGGER = logging.getLogger("sentinel")


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    state_directory: Path
    listen_address: str
    listen_port: int
    log_level: str

    @property
    def state_file(self) -> Path:
        return self.state_directory / "status.json"


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    LOGGER.handlers.clear()
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)
    LOGGER.propagate = False


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

    required = (("storage", "state_directory"), ("server", "listen_address"))
    for section, option in required:
        if not parser.has_option(section, option):
            raise ConfigurationError(f"option requise: [{section}] {option}")

    configured = Path(parser.get("storage", "state_directory")).expanduser()
    if not configured.is_absolute():
        configured = config_path.resolve().parent / configured

    try:
        listen_port = parser.getint("server", "listen_port")
    except (configparser.Error, ValueError) as exc:
        raise ConfigurationError("[server] listen_port doit être un entier") from exc
    if not 1 <= listen_port <= 65535:
        raise ConfigurationError("[server] listen_port doit être compris entre 1 et 65535")

    listen_address = parser.get("server", "listen_address").strip()
    if not listen_address:
        raise ConfigurationError("[server] listen_address ne peut pas être vide")

    log_level = parser.get("logging", "level", fallback="INFO").upper()
    if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ConfigurationError("[logging] level invalide")

    return Settings(configured.resolve(), listen_address, listen_port, log_level)


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


def is_ready(settings: Settings) -> bool:
    return (
        settings.state_file.is_file()
        and os.access(settings.state_file, os.R_OK)
        and os.access(settings.state_directory, os.W_OK)
    )


class SentinelServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], settings: Settings):
        self.settings = settings
        super().__init__(address, SentinelHandler)


class SentinelHandler(BaseHTTPRequestHandler):
    server: SentinelServer
    server_version = f"Sentinel/{VERSION}"
    sys_version = ""

    def send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.partition("?")[0]
        if path == "/health":
            self.send_json(HTTPStatus.OK, {"status": "ok", "version": VERSION})
            return
        if path == "/ready":
            ready = is_ready(self.server.settings)
            code = HTTPStatus.OK if ready else HTTPStatus.SERVICE_UNAVAILABLE
            self.send_json(code, {"status": "ready" if ready else "not-ready"})
            return
        if path == "/api/v1/status":
            try:
                self.send_json(HTTPStatus.OK, read_status(self.server.settings))
            except (OSError, RuntimeError, json.JSONDecodeError) as exc:
                self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "error", "detail": str(exc)})
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"status": "error", "detail": "route inconnue"})

    def log_message(self, message: str, *args: object) -> None:
        LOGGER.info("client=%s message=%s", self.client_address[0], message % args)


def create_server(settings: Settings) -> SentinelServer:
    return SentinelServer((settings.listen_address, settings.listen_port), settings)


def sd_notify(message: str, environment: dict[str, str] | None = None) -> bool:
    env = os.environ if environment is None else environment
    address = env.get("NOTIFY_SOCKET")
    if not address:
        return False
    if address.startswith("@"):
        address = "\0" + address[1:]
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as notifier:
        notifier.connect(address)
        notifier.sendall(message.encode("utf-8"))
    return True


def serve(settings: Settings) -> None:
    write_status(settings, collect_status())
    stop = threading.Event()

    def request_stop(signum: int, _frame: object) -> None:
        LOGGER.info("arrêt demandé signal=%s", signum)
        stop.set()

    previous_term = signal.signal(signal.SIGTERM, request_stop)
    previous_int = signal.signal(signal.SIGINT, request_stop)
    try:
        with create_server(settings) as server:
            server.timeout = 0.5
            LOGGER.info("écoute sur %s:%s", *server.server_address)
            sd_notify("READY=1\nSTATUS=Sentinel accepte les requêtes")
            while not stop.is_set():
                server.handle_request()
                sd_notify("WATCHDOG=1")
            sd_notify("STOPPING=1\nSTATUS=Arrêt de Sentinel")
    finally:
        signal.signal(signal.SIGTERM, previous_term)
        signal.signal(signal.SIGINT, previous_int)


def healthcheck(settings: Settings) -> bool:
    host = settings.listen_address
    if host in {"0.0.0.0", "::"}:
        host = "127.0.0.1"
    url = f"http://{host}:{settings.listen_port}/ready"
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            payload = json.load(response)
        return response.status == 200 and payload.get("status") == "ready"
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sentinel")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--config", type=Path, default=Path("config/sentinel.conf"))
    parser.add_argument("--check-config", action="store_true")
    parser.add_argument("--healthcheck", action="store_true")
    commands = parser.add_subparsers(dest="command")
    status = commands.add_parser("status")
    status.add_argument("--format", choices=("text", "json"), default="text")
    commands.add_parser("record")
    show = commands.add_parser("show")
    show.add_argument("--format", choices=("text", "json"), default="text")
    commands.add_parser("serve")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
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
        configure_logging(settings.log_level)
        if args.healthcheck:
            return 0 if healthcheck(settings) else 1
        if args.command == "record":
            write_status(settings, collect_status())
            print(settings.state_file)
            return 0
        if args.command == "show":
            print(render_status(read_status(settings), args.format))
            return 0
        if args.command == "serve":
            serve(settings)
            return 0
    except (ConfigurationError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"sentinel: {exc}", file=sys.stderr)
        return 1

    build_parser().print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
