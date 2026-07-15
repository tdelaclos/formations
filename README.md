# Partie I — Construire un socle sécurisé
## Campagne 1 — Installation et fondations
### 1.1 Pourquoi sécuriser un socle Linux ?
### 1.2 Installation d'AlmaLinux minimal
### 1.3 Comprendre les composants d'un système Linux
### 1.4 Premier démarrage et premières vérifications
### 1.5 Mise à jour et gestion des dépôts
### 1.6 Architecture des systèmes de fichiers
### 1.7 Utilisateurs, groupes et permissions
### 1.8 sudo et principe du moindre privilège
### 1.9 Première mise en sécurité du serveur
### 1.10 Création du laboratoire Sentinel
## Campagne 2 — Contrôle des accès
### 2.1 Les permissions UNIX
### 2.2 ACL
### 2.3 umask
### 2.4 Attributs étendus (chattr)
### 2.5 PAM
### 2.6 Politique de mots de passe
### 2.7 Comptes système
### 2.8 sudo avancé
### 2.9 Comprendre /etc/passwd, /etc/shadow et /etc/group
### 2.10 Synthèse : sécuriser les identités
## Campagne 3 — Réseau et exposition
### 3.1 TCP/IP côté administrateur
### 3.2 Firewalld : architecture
### 3.3 Les zones Firewalld
### 3.4 Les services Firewalld
### 3.5 Les ports et protocoles
### 3.6 Runtime vs Permanent
### 3.7 Rich Rules
### 3.8 NAT et Port Forwarding
### 3.9 Journalisation et diagnostic
### 3.10 Construction de la politique réseau de Sentinel
## Campagne 4 — SSH et accès distant
### 4.1 Architecture d'OpenSSH
### 4.2 Authentification par mot de passe
### 4.3 Authentification par clés
### 4.4 Durcissement de sshd_config
### 4.5 Bastion d'administration
### 4.6 Journalisation et audit SSH
### 4.7 Protection contre les attaques (Fail2ban, etc.)
### 4.8 Mission : administration sécurisée de Sentinel
## Campagne 5 — Systemd et les services
### 5.1 Comprendre systemd
### 5.2 Les unités (.service, .socket, .target…)
### 5.3 Créer le service Sentinel
### 5.4 Sandboxing systemd
### 5.5 Capacités Linux
### 5.6 Journalisation avec journald
### 5.7 Supervision et redémarrage automatique
### 5.8 Mission : rendre Sentinel résilient
## Campagne 6 — SELinux
### 6.1 Pourquoi SELinux existe
### 6.2 Les contextes
### 6.3 Les politiques
### 6.4 Diagnostic des refus
### 6.5 Création de règles
### 6.6 Sécuriser Sentinel avec SELinux
## Campagne 7 — TLS et PKI
### 7.1 Cryptographie appliquée
### 7.2 Certificats X.509
### 7.3 Autorité de certification
### 7.4 Mutual TLS
### 7.5 Intégration FreeIPA
### 7.6 Rotation des certificats
### 7.7 Sécurisation TLS de Sentinel
# Partie II — Industrialiser la sécurité
## Campagne 8 — FreeIPA
### 8.1 Présentation de FreeIPA
### 8.2 Architecture interne (389 DS, Kerberos, Dogtag, DNS…)
### 8.3 Installation
### 8.4 Gestion des utilisateurs
### 8.5 Groupes et rôles
### 8.6 Politiques sudo
### 8.7 Gestion des hôtes
### 8.8 Certificats
### 8.9 Intégration de Sentinel
### 8.10 Mission : administrer une infrastructure avec FreeIPA
## Campagne 9 — Ansible
### 9.1 Architecture Ansible
### 9.2 Inventaires
### 9.3 Playbooks
### 9.4 Variables
### 9.5 Rôles
### 9.6 Vault
### 9.7 Déploiement de Sentinel
### 9.8 Durcissement automatisé
### 9.9 Vérification de conformité
### 9.10 Mission : reconstruire un serveur en moins de 30 minutes
## Campagne 10 — RPM et cycle de vie
### 10.1 Construire un paquet RPM
### 10.2 Dépendances
### 10.3 Fichiers de configuration
### 10.4 Signature des paquets
### 10.5 Dépôt RPM privé
### 10.6 Packaging de Sentinel
## Campagne 11 — Conteneurisation
### 11.1 Podman
### 11.2 Rootless
### 11.3 Images sécurisées
### 11.4 Réseaux
### 11.5 Secrets
### 11.6 Exécution sécurisée de Sentinel
## Campagne 12 — Supervision et audit
### 12.1 Journalisation centralisée
### 12.2 Auditd
### 12.3 Intégrité des fichiers
### 12.4 Supervision
### 12.5 Alertes
### 12.6 Tableau de bord Sentinel
# Partie III — Mise en situation
## Campagne 13 — Attaques et défense

Chaque chapitre suit le même principe :

Présentation de l'attaque

Réalisation depuis Kali Linux

Analyse des traces

Mise en œuvre des contre-mesures

Vérification de l'efficacité

### 13.1 Reconnaissance
### 13.2 Scan réseau
### 13.3 Brute force SSH
### 13.4 Escalade de privilèges
### 13.5 Mouvements latéraux
### 13.6 Persistance
### 13.7 Exfiltration
### 13.8 Étude de cas complète
## Campagne 14 — Projet final
### 14.1 Déployer Sentinel sur une AlmaLinux minimale
### 14.2 Sécuriser l'hôte
### 14.3 Intégrer FreeIPA
### 14.4 Déployer avec Ansible
### 14.5 Packager en RPM
### 14.6 Conteneuriser avec Podman
### 14.7 Superviser et auditer
### 14.8 Audit final et tests d'intrusion depuis Kali
