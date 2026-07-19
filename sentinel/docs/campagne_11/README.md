# Campagne 11 — Conteneurisation

Cette campagne transforme l'image Sentinel en service Podman rootless géré par Quadlet. Elle couvre le moteur, les user namespaces, la chaîne de confiance des images, les flux réseau, les secrets et le cycle de vie de production.

## Parcours

1. [Découvrir Podman](11.1-decouvrir-podman.md) ;
2. [exécuter des conteneurs rootless](11.2-conteneurs-rootless.md) ;
3. [construire des images sécurisées](11.3-construire-images-securisees.md) ;
4. [concevoir les réseaux de conteneurs](11.4-reseaux-conteneurs.md) ;
5. [gérer les secrets avec Podman](11.5-gerer-secrets-podman.md) ;
6. [exécuter Sentinel en sécurité](11.6-executer-sentinel-securite.md).

## Résultat attendu

À la fin de la campagne, l'apprenant dispose d'une image Sentinel minimale et signée, exécutée sans privilège par un compte dédié, déclarée avec Quadlet et testée pour la mise à jour, le rollback, le confinement et les flux autorisés depuis Kali.

Les chapitres suivent le formalisme défini dans le [`GUIDE-REDACTION.md`](../GUIDE-REDACTION.md).
