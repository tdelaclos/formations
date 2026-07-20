"""Cycle de vie systemd et healthcheck compatible mTLS."""

import json
import os
import signal
import socket
import threading
import urllib.error
import urllib.request
from typing import Optional

from configuration import Settings
from diagnostic import collect_status
from logging_support import LOGGER
from state import write_status
from tls_support import create_healthcheck_context
from web import create_server


def sd_notify(message: str, environment: Optional[dict[str, str]] = None) -> bool:
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
    # server_name vérifie le SAN même si le service écoute sur une adresse IP.
    host = settings.healthcheck_server_name or settings.listen_address
    if host in {"0.0.0.0", "::"}:
        host = "127.0.0.1"
    scheme = "https" if settings.tls_enabled else "http"
    context = create_healthcheck_context(settings) if settings.tls_enabled else None
    try:
        url = f"{scheme}://{host}:{settings.listen_port}/ready"
        with urllib.request.urlopen(
            url, timeout=2, context=context
        ) as response:
            payload = json.load(response)
        return response.status == 200 and payload.get("status") == "ready"
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return False
