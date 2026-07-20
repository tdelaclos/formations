# Campagne 7 — TLS et PKI

Cette campagne protège les échanges de Sentinel et donne à l'apprenant les bases nécessaires pour administrer des certificats. Elle part des primitives cryptographiques, construit une chaîne de confiance de laboratoire, introduit l'authentification mutuelle et termine par le jalon Sentinel `0.5.0`.

## Parcours

1. [Comprendre la cryptographie appliquée](7.1-comprendre-cryptographie-appliquee.md) ;
2. [lire et vérifier un certificat X.509](7.2-lire-verifier-certificats-x509.md) ;
3. [construire une autorité de certification](7.3-construire-autorite-certification.md) ;
4. [authentifier les deux extrémités avec mTLS](7.4-authentification-mutuelle-tls.md) ;
5. [préparer l'intégration à FreeIPA](7.5-preparer-integration-freeipa.md) ;
6. [renouveler et révoquer les certificats](7.6-renouveler-revoquer-certificats.md) ;
7. [sécuriser Sentinel avec TLS](7.7-securiser-sentinel-tls.md).

## Résultat attendu

À la fin de la campagne, l'apprenant dispose d'une PKI de laboratoire, sait distinguer certificat, clé privée et ancre de confiance, peut diagnostiquer une chaîne X.509 et exploite Sentinel `0.5.0` avec TLS ou mTLS. Il sait également préparer le renouvellement sans désactiver la vérification du pair.

Les chapitres suivent le formalisme défini dans le [`GUIDE-REDACTION.md`](../GUIDE-REDACTION.md).
