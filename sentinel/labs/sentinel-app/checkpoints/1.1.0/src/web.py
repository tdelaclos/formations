"""API HTTP instrumentée par les métriques de la campagne 12."""

import json
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from configuration import Settings
from identity import is_authorized_certificate
from logging_support import LOGGER
from metrics import Metrics
from state import is_ready, read_status
from tls_support import create_server_context
from version import VERSION


class SentinelServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], settings: Settings):
        self.settings = settings
        self.metrics = Metrics()
        super().__init__(address, SentinelHandler)


class SentinelHandler(BaseHTTPRequestHandler):
    server: SentinelServer
    server_version = f"Sentinel/{VERSION}"
    sys_version = ""

    def send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        self.response_status = int(status)
        body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_metrics(self) -> None:
        body = self.server.metrics.render(self.server.settings).encode("utf-8")
        self.response_status = int(HTTPStatus.OK)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.partition("?")[0]
        # Une valeur arbitraire est regroupée sous "unknown" pour borner les séries.
        route = path if path in {"/health", "/ready", "/api/v1/status", "/metrics"} else "unknown"
        started = time.monotonic()
        self.response_status = int(HTTPStatus.INTERNAL_SERVER_ERROR)
        self.server.metrics.start_request()
        try:
            self.handle_get(path)
        finally:
            self.server.metrics.finish_request(route, self.response_status, time.monotonic() - started)

    def handle_get(self, path: str) -> None:
        settings = self.server.settings
        if settings.tls_enabled and settings.tls_require_client_certificate:
            certificate = self.connection.getpeercert()
            if not is_authorized_certificate(certificate, settings.allowed_dns_names):
                self.send_json(HTTPStatus.FORBIDDEN, {"status": "error", "detail": "identité cliente non autorisée"})
                return
        if path == "/metrics":
            # L'observabilité conserve exactement les contrôles mTLS de l'API.
            self.send_metrics()
        elif path == "/health":
            self.send_json(HTTPStatus.OK, {"status": "ok", "version": VERSION})
        elif path == "/ready":
            ready = is_ready(settings)
            code = HTTPStatus.OK if ready else HTTPStatus.SERVICE_UNAVAILABLE
            self.send_json(code, {"status": "ready" if ready else "not-ready"})
        elif path == "/api/v1/status":
            try:
                self.send_json(HTTPStatus.OK, read_status(settings))
            except (OSError, RuntimeError, json.JSONDecodeError) as exc:
                self.send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"status": "error", "detail": str(exc)})
        else:
            self.send_json(HTTPStatus.NOT_FOUND, {"status": "error", "detail": "route inconnue"})

    def log_message(self, message: str, *args: object) -> None:
        LOGGER.info("client=%s message=%s", self.client_address[0], message % args)


def create_server(settings: Settings) -> SentinelServer:
    server = SentinelServer((settings.listen_address, settings.listen_port), settings)
    if settings.tls_enabled:
        server.socket = create_server_context(settings).wrap_socket(server.socket, server_side=True)
    return server
