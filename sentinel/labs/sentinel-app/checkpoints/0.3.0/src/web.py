"""Interface HTTP ajoutée pour mettre en pratique TCP/IP et Firewalld."""

import json
import logging
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from configuration import Settings
from state import read_status
from version import VERSION


class SentinelServer(ThreadingHTTPServer):
    """Associe la configuration validée aux gestionnaires de requêtes."""

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

    def do_GET(self) -> None:  # noqa: N802 - nom imposé par la bibliothèque HTTP
        # Une route explicite rend les flux réseau prévisibles pour Firewalld.
        path = self.path.partition("?")[0]
        if path == "/health":
            self.send_json(HTTPStatus.OK, {"status": "ok", "version": VERSION})
            return
        if path == "/api/v1/status":
            try:
                self.send_json(HTTPStatus.OK, read_status(self.server.settings))
            except (OSError, RuntimeError, json.JSONDecodeError) as exc:
                self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "error", "detail": str(exc)})
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"status": "error", "detail": "route inconnue"})

    def log_message(self, message: str, *args: object) -> None:
        logging.info("client=%s message=%s", self.client_address[0], message % args)


def create_server(settings: Settings) -> SentinelServer:
    return SentinelServer((settings.listen_address, settings.listen_port), settings)
