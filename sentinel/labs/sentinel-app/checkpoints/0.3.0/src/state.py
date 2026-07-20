"""État persistant dont les permissions ont été définies en campagne 2."""

import json
import os
import tempfile
from pathlib import Path

from configuration import Settings


def write_status(settings: Settings, status: dict[str, str]) -> None:
    settings.state_directory.mkdir(mode=0o750, parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=settings.state_directory, prefix=".status-", text=True
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
