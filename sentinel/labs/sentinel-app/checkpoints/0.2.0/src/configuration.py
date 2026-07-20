"""Validation de la configuration introduite par la campagne 2."""

import configparser
from dataclasses import dataclass
from pathlib import Path


class ConfigurationError(ValueError):
    """Signale une configuration absente ou invalide."""


@dataclass(frozen=True)
class Settings:
    """Configuration validée, distincte du parseur de fichier INI."""

    state_directory: Path

    @property
    def state_file(self) -> Path:
        return self.state_directory / "status.json"


def load_settings(config_path: Path) -> Settings:
    """Charge le fichier sans interpolation implicite de valeurs."""

    parser = configparser.ConfigParser(interpolation=None)
    if not parser.read(config_path, encoding="utf-8"):
        raise ConfigurationError(f"configuration introuvable: {config_path}")

    if not parser.has_option("storage", "state_directory"):
        raise ConfigurationError("option requise: [storage] state_directory")

    configured = Path(parser.get("storage", "state_directory")).expanduser()
    if not configured.is_absolute():
        # Un chemin relatif suit le fichier de configuration, pas le cwd.
        configured = config_path.resolve().parent / configured

    return Settings(state_directory=configured.resolve())
