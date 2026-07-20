"""Persistance et permissions mises en pratique pendant la campagne 2."""

import json
import os
import tempfile
from pathlib import Path

from configuration import Settings


def write_status(settings: Settings, status: dict[str, str]) -> None:
    """Écrit l'état de façon atomique avec un mode explicite 0640."""

    settings.state_directory.mkdir(mode=0o750, parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=settings.state_directory,
        prefix=".status-",
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        # La campagne 2 montre pourquoi l'umask seul ne suffit pas à un contrat.
        os.fchmod(descriptor, 0o640)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(status, stream, ensure_ascii=False, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        # Le temporaire est créé dans le même répertoire pour garantir le rename.
        os.replace(temporary, settings.state_file)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def read_status(settings: Settings) -> dict[str, str]:
    """Relit un état Sentinel et refuse un document d'une autre application."""

    try:
        with settings.state_file.open(encoding="utf-8") as stream:
            payload = json.load(stream)
    except FileNotFoundError as exc:
        raise RuntimeError("aucun état enregistré") from exc

    if not isinstance(payload, dict) or payload.get("application") != "sentinel":
        raise RuntimeError("état Sentinel invalide")
    return {str(key): str(value) for key, value in payload.items()}
