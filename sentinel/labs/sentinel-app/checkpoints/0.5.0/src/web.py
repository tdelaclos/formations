"""API HTTP existante, maintenant enveloppée par TLS/mTLS."""

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from configuration import Settings
from logging_support import LOGGER
from state import is_ready, read_status
from tls_support import create_server_context
from version import VERSION


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
        elif path == "/ready":
            ready = is_ready(self.server.settings)
            code = HTTPStatus.OK if ready else HTTPStatus.SERVICE_UNAVAILABLE
            self.send_json(code, {"status": "ready" if ready else "not-ready"})
        elif path == "/api/v1/status":
            try:
                self.send_json(HTTPStatus.OK, read_status(self.server.settings))
            except (OSError, RuntimeError, json.JSONDecodeError) as exc:
                self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "error", "detail": str(exc)})
        else:
            self.send_json(HTTPStatus.NOT_FOUND, {"status": "error", "detail": "route inconnue"})

    def log_message(self, message: str, *args: object) -> None:
        LOGGER.info("client=%s message=%s", self.client_address[0], message % args)


def create_server(settings: Settings) -> SentinelServer:
    server = SentinelServer((settings.listen_address, settings.listen_port), settings)
    if settings.tls_enabled:
        # La socket applicative ne change pas ; TLS protège son transport.
        server.socket = create_server_context(settings).wrap_socket(server.socket, server_side=True)
    return server
