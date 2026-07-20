"""Cycle de vie systemd, signaux et healthcheck introduits en campagne 5."""

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
from web import create_server


def sd_notify(message: str, environment: Optional[dict[str, str]] = None) -> bool:
    """Parle directement au socket de notification fourni par systemd."""

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
    """Accepte SIGTERM proprement et alimente le watchdog systemd."""

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
    host = "127.0.0.1" if settings.listen_address in {"0.0.0.0", "::"} else settings.listen_address
    try:
        with urllib.request.urlopen(f"http://{host}:{settings.listen_port}/ready", timeout=2) as response:
            payload = json.load(response)
        return response.status == 200 and payload.get("status") == "ready"
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return False
