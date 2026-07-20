"""Configuration enrichie du niveau de journalisation en campagne 5."""

import configparser
from dataclasses import dataclass
from pathlib import Path


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    state_directory: Path
    listen_address: str
    listen_port: int
    log_level: str

    @property
    def state_file(self) -> Path:
        return self.state_directory / "status.json"


def load_settings(config_path: Path) -> Settings:
    parser = configparser.ConfigParser(interpolation=None)
    if not parser.read(config_path, encoding="utf-8"):
        raise ConfigurationError(f"configuration introuvable: {config_path}")
    for section, option in (("storage", "state_directory"), ("server", "listen_address")):
        if not parser.has_option(section, option):
            raise ConfigurationError(f"option requise: [{section}] {option}")

    configured = Path(parser.get("storage", "state_directory")).expanduser()
    if not configured.is_absolute():
        configured = config_path.resolve().parent / configured
    try:
        listen_port = parser.getint("server", "listen_port")
    except (configparser.Error, ValueError) as exc:
        raise ConfigurationError("[server] listen_port doit être un entier") from exc
    if not 1 <= listen_port <= 65535:
        raise ConfigurationError("[server] listen_port doit être compris entre 1 et 65535")

    listen_address = parser.get("server", "listen_address").strip()
    if not listen_address:
        raise ConfigurationError("[server] listen_address ne peut pas être vide")
    log_level = parser.get("logging", "level", fallback="INFO").upper()
    if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise ConfigurationError("[logging] level invalide")
    return Settings(configured.resolve(), listen_address, listen_port, log_level)
