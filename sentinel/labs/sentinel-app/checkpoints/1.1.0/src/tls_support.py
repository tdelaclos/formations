"""Contextes TLS serveur et client étudiés pendant la campagne 7."""

import ssl

from configuration import Settings


def create_server_context(settings: Settings) -> ssl.SSLContext:
    """Construit le contexte serveur et impose le certificat client si demandé."""

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(settings.tls_certificate, settings.tls_private_key)
    if settings.tls_client_ca is not None:
        context.load_verify_locations(cafile=settings.tls_client_ca)
    context.verify_mode = ssl.CERT_REQUIRED if settings.tls_require_client_certificate else ssl.CERT_NONE
    return context


def create_healthcheck_context(settings: Settings) -> ssl.SSLContext:
    """Vérifie le serveur et présente l'identité cliente du healthcheck."""

    context = ssl.create_default_context(cafile=settings.tls_client_ca)
    if settings.healthcheck_certificate and settings.healthcheck_private_key:
        context.load_cert_chain(settings.healthcheck_certificate, settings.healthcheck_private_key)
    return context
