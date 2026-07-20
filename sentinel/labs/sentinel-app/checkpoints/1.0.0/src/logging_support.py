"""Journaux JSON transmis à journald depuis la campagne 5."""

import json
import logging
from datetime import datetime, timezone

LOGGER = logging.getLogger("sentinel")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname, "logger": record.name,
            "message": record.getMessage(),
        }, ensure_ascii=False, sort_keys=True)


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    LOGGER.handlers.clear()
    LOGGER.addHandler(handler)
    LOGGER.setLevel(level)
    LOGGER.propagate = False
