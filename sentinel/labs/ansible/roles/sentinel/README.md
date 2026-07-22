# Rôle `sentinel`

Ce rôle déploie le checkpoint Sentinel `0.6.0` depuis le dépôt de formation.

Il garantit le compte système, les répertoires, les sources, la configuration validée, l'unité systemd et les vérifications fonctionnelles. Il ne crée pas le domaine FreeIPA, ne transporte aucune clé privée et ne désactive aucune protection Linux.

Variables principales :

| Variable | Défaut | Fonction |
|---|---|---|
| `sentinel_version` | `0.6.0` | checkpoint accepté |
| `sentinel_source_checkpoint` | chemin calculé depuis le playbook | source locale du produit |
| `sentinel_listen_port` | `8443` | port d'écoute |
| `sentinel_tls_enabled` | `false` | activation après provisionnement des certificats |
| `sentinel_allowed_dns_names` | liste du laboratoire | identités mTLS autorisées |

Le rôle cible les distributions compatibles RHEL 9 ou ultérieures. Relancez-le sans modifier ses entrées pour vérifier `changed=0`.
