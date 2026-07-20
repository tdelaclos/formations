"""Diagnostic local conservé depuis la campagne 1."""

import json
import platform
import socket

from version import VERSION


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
