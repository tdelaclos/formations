"""Autorisation applicative ajoutée après l'authentification mTLS en campagne 8."""

from typing import Any


def certificate_dns_names(certificate: dict[str, Any]) -> set[str]:
    """Ne retient que les identités DNS du SAN, jamais le CN historique."""

    return {
        str(value).lower()
        for name_type, value in certificate.get("subjectAltName", ())
        if name_type == "DNS"
    }


def is_authorized_certificate(
    certificate: dict[str, Any], allowed_dns_names: tuple[str, ...]
) -> bool:
    """Sépare certificat de confiance et identité explicitement autorisée."""

    return bool(certificate_dns_names(certificate).intersection(allowed_dns_names))
