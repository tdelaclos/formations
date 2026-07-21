# Formation Sentinel

Ce dépôt contient une formation progressive à l'administration et à la sécurité d'un socle AlmaLinux. Une application Python appelée **Sentinel** sert de fil rouge : elle commence comme un diagnostic local, devient un service réseau, puis est confinée, chiffrée, automatisée, empaquetée, conteneurisée et supervisée.

## Lire la formation sur GitHub

Les liens suivants permettent de commencer sans installer d'outil :

- [page d'accueil et présentation du parcours](sentinel/docs/index.md) ;
- [sommaire complet des chapitres](sentinel/docs/README.md) ;
- [premier chapitre](sentinel/docs/campagne_01/1.1-pourquoi-securiser-socle-linux.md) ;
- [trajectoire de l'application Sentinel](sentinel/docs/PARCOURS-SENTINEL.md) ;
- [code et tests des checkpoints](sentinel/labs/sentinel-app/README.md).

Les campagnes 1 à 12 sont disponibles. Les campagnes 13, consacrée aux scénarios d'attaque et de défense, et 14, consacrée au projet final, restent prévues mais ne sont pas encore rédigées.

## Parcours disponible

| Campagne | Sujet | Résultat principal |
| --- | --- | --- |
| [1](sentinel/docs/campagne_01/1.1-pourquoi-securiser-socle-linux.md) | installation et fondations | AlmaLinux minimal et Sentinel `0.1.0` |
| [2](sentinel/docs/campagne_02/2.1-permissions-unix.md) | permissions et identités | configuration et état contrôlés |
| [3](sentinel/docs/campagne_03/3.1-tcp-ip-administrateur.md) | TCP/IP et Firewalld | API Sentinel exposée selon une matrice de flux |
| [4](sentinel/docs/campagne_04/4.1-architecture-openssh.md) | OpenSSH | administration distante durcie |
| [5](sentinel/docs/campagne_05/5.1-comprendre-systemd.md) | systemd | service durable, observable et relançable |
| [6](sentinel/docs/campagne_06/6.1-pourquoi-selinux-existe.md) | SELinux | processus Sentinel confiné |
| [7](sentinel/docs/campagne_07/7.1-comprendre-cryptographie-appliquee.md) | TLS et PKI | canal TLS ou mTLS et Sentinel `0.5.0` |
| [8](sentinel/docs/campagne_08/8.1-presentation-freeipa.md) | FreeIPA | identités et certificats centralisés |
| [9](sentinel/docs/campagne_09/9.1-pourquoi-automatiser-avec-ansible.md) | Ansible | déploiement multi-hôte reproductible |
| [10](sentinel/docs/campagne_10/10.1-construire-paquet-rpm.md) | RPM | paquet signé et dépôt privé |
| [11](sentinel/docs/campagne_11/11.1-decouvrir-podman.md) | Podman | exécution rootless de Sentinel |
| [12](sentinel/docs/campagne_12/12.1-centraliser-journaux-rsyslog.md) | supervision et audit | journaux, audit, intégrité, métriques et alertes |

## Utiliser le site MkDocs

Le rendu MkDocs fournit la navigation latérale et la recherche.

### Préparer un environnement isolé

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install mkdocs mkdocs-mermaid2-plugin
```

### Lire localement

```bash
mkdocs serve -f sentinel/mkdocs.yml
```

Ouvrez ensuite l'adresse indiquée par MkDocs, généralement `http://127.0.0.1:8000/`.

### Construire le site statique

```bash
mkdocs build -f sentinel/mkdocs.yml
```

Le résultat est produit dans `sentinel/site/`. Ce répertoire généré n'est pas une source à modifier manuellement.

## Utiliser les checkpoints Sentinel

Chaque checkpoint est autonome et contient son code, sa configuration de référence et ses tests.

```bash
cd sentinel/labs/sentinel-app/checkpoints/0.5.0
python3 src/sentinel.py --version
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 -m unittest discover -s tests -v
```

Consultez le [README de l'application](sentinel/labs/sentinel-app/README.md) pour connaître les responsabilités des modules et la progression entre les versions.

## Organisation du dépôt

```text
.
├── README.md
└── sentinel/
    ├── mkdocs.yml
    ├── docs/
    │   ├── index.md
    │   ├── GUIDE-REDACTION.md
    │   ├── PARCOURS-SENTINEL.md
    │   └── campagne_01/ ... campagne_12/
    └── labs/
        └── sentinel-app/
            └── checkpoints/
```

## Contribuer ou relire

Le [`GUIDE-REDACTION.md`](sentinel/docs/GUIDE-REDACTION.md) définit le nommage, la structure des chapitres, l'usage de Mermaid et les contrôles avant publication.

Avant de proposer une modification :

```bash
git diff --check
mkdocs build -f sentinel/mkdocs.yml
```

Si le code Sentinel est touché, exécutez également les tests du checkpoint modifié et vérifiez que les interfaces acquises par les versions précédentes restent disponibles.
