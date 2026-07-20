"""Journaux JSON envoyés sur stdout pour être collectés par journald."""

import json
import logging
from datetime import datetime, timezone


LOGGER = logging.getLogger("sentinel")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def configure_logging(level: str) -> None:
    """Laisse systemd décider de la destination finale des journaux."""

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    LOGGER.handlers.clear()
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)
    LOGGER.propagate = False
