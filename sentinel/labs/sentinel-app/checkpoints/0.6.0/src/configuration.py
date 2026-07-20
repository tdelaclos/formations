"""Configuration TLS et liste fermée d'identités de la campagne 8."""

import configparser
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    state_directory: Path
    listen_address: str
    listen_port: int
    log_level: str
    tls_enabled: bool = False
    tls_certificate: Optional[Path] = None
    tls_private_key: Optional[Path] = None
    tls_client_ca: Optional[Path] = None
    tls_require_client_certificate: bool = False
    healthcheck_certificate: Optional[Path] = None
    healthcheck_private_key: Optional[Path] = None
    allowed_dns_names: tuple[str, ...] = ()
    healthcheck_server_name: Optional[str] = None

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

    state_directory = Path(parser.get("storage", "state_directory")).expanduser()
    if not state_directory.is_absolute():
        state_directory = config_path.resolve().parent / state_directory
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

    def configured_path(section: str, option: str) -> Optional[Path]:
        value = parser.get(section, option, fallback="").strip()
        if not value:
            return None
        path = Path(value).expanduser()
        return (config_path.resolve().parent / path).resolve() if not path.is_absolute() else path.resolve()

    tls_enabled = parser.getboolean("tls", "enabled", fallback=False)
    require_client = parser.getboolean("tls", "require_client_certificate", fallback=False)
    certificate = configured_path("tls", "certificate")
    private_key = configured_path("tls", "private_key")
    client_ca = configured_path("tls", "client_ca")
    health_certificate = configured_path("healthcheck", "certificate")
    health_private_key = configured_path("healthcheck", "private_key")
    health_server_name = parser.get("healthcheck", "server_name", fallback="").strip() or None
    allowed_dns_names = tuple(
        name.strip().lower()
        for name in parser.get("identity", "allowed_dns_names", fallback="").split(",")
        if name.strip()
    )

    if tls_enabled:
        # Un service ne doit jamais démarrer en clair parce qu'un fichier manque.
        required = [certificate, private_key]
        if require_client:
            required.extend([client_ca, health_certificate, health_private_key])
        if any(path is None or not path.is_file() for path in required):
            raise ConfigurationError("fichier TLS requis absent ou illisible")
        if require_client and not allowed_dns_names:
            raise ConfigurationError(
                "[identity] allowed_dns_names requis lorsque le mTLS est actif"
            )

    return Settings(
        state_directory.resolve(), listen_address, listen_port, log_level,
        tls_enabled, certificate, private_key, client_ca, require_client,
        health_certificate, health_private_key, allowed_dns_names,
        health_server_name,
    )
