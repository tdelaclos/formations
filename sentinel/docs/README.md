# Formation Sentinel — sécuriser et industrialiser AlmaLinux

Ce fichier est le sommaire pratique destiné à la lecture directe depuis GitHub. La [page d'accueil](index.md) présente les objectifs, la méthode et le fil rouge ; la liste ci-dessous donne un accès direct à chaque chapitre.

Les campagnes 1 à 14 sont rédigées. La campagne 13 utilise des scénarios d’attaque strictement bornés afin d’exercer la détection, le confinement, la corrélation et la remédiation sans introduire de vulnérabilité volontaire dans Sentinel. Le formalisme commun est décrit dans le [guide de rédaction](GUIDE-REDACTION.md) et les versions de l'application dans le [parcours Sentinel](PARCOURS-SENTINEL.md).

## Partie I — Construire un socle sécurisé

### Campagne 1 — Installation et fondations

- [1.1 — Pourquoi sécuriser un socle Linux ?](campagne_01/1.1-pourquoi-securiser-socle-linux.md)
- [1.2 — Installer AlmaLinux minimal](campagne_01/1.2-installation-almalinux-minimal.md)
- [1.3 — Comprendre les composants d'un système Linux](campagne_01/1.3-composants-systeme-linux.md)
- [1.4 — Établir la baseline du serveur](campagne_01/1.4-premier-demarrage-verifications.md)
- [1.5 — Mettre à jour et gérer les dépôts](campagne_01/1.5-mise-a-jour-gestion-depots.md)
- [1.6 — Organiser les systèmes de fichiers](campagne_01/1.6-architecture-systemes-fichiers.md)
- [1.7 — Comprendre identités et permissions](campagne_01/1.7-utilisateurs-groupes-permissions.md)
- [1.8 — Administrer avec `sudo`](campagne_01/1.8-sudo-moindre-privilege.md)
- [1.9 — Mission : mettre le serveur en sécurité](campagne_01/1.9-premiere-mise-en-securite-serveur.md)
- [1.10 — Créer le laboratoire Sentinel](campagne_01/1.10-creation-laboratoire-sentinel.md)

### Campagne 2 — Contrôle des accès

- [2.1 — Les permissions UNIX](campagne_02/2.1-permissions-unix.md)
- [2.2 — Les ACL](campagne_02/2.2-acl.md)
- [2.3 — L'`umask`](campagne_02/2.3-umask.md)
- [2.4 — Les attributs étendus](campagne_02/2.4-attributs-etendus.md)
- [2.5 — PAM](campagne_02/2.5-pam.md)
- [2.6 — Politique de mots de passe](campagne_02/2.6-politique-mots-de-passe.md)
- [2.7 — Les comptes système](campagne_02/2.7-comptes-systeme.md)
- [2.8 — `sudo` avancé](campagne_02/2.8-sudo-avance.md)
- [2.9 — Comprendre les fichiers d'identités Linux](campagne_02/2.9-fichiers-identites-linux.md)
- [2.10 — Synthèse : sécuriser les identités](campagne_02/2.10-synthese-securiser-identites.md)

### Campagne 3 — Réseau et exposition

- [3.1 — TCP/IP côté administrateur](campagne_03/3.1-tcp-ip-administrateur.md)
- [3.2 — Architecture de Firewalld](campagne_03/3.2-architecture-firewalld.md)
- [3.3 — Les zones Firewalld](campagne_03/3.3-zones-firewalld.md)
- [3.4 — Les services Firewalld](campagne_03/3.4-services-firewalld.md)
- [3.5 — Conntrack et le filtrage par états](campagne_03/3.5-conntrack-filtrage-etats.md)
- [3.6 — Les Rich Rules Firewalld](campagne_03/3.6-rich-rules-firewalld.md)
- [3.7 — Journalisation et analyse Firewalld](campagne_03/3.7-journalisation-firewalld.md)
- [3.8 — Les IP Sets Firewalld](campagne_03/3.8-ip-sets-firewalld.md)
- [3.9 — Runtime et Permanent](campagne_03/3.9-runtime-permanent.md)
- [3.10 — Concevoir la politique réseau de Sentinel](campagne_03/3.10-politique-reseau-sentinel.md)

### Campagne 4 — SSH et accès distant

- [4.1 — Architecture d'OpenSSH](campagne_04/4.1-architecture-openssh.md)
- [4.2 — Authentification par mot de passe](campagne_04/4.2-authentification-mot-de-passe.md)
- [4.3 — Authentification par clés](campagne_04/4.3-authentification-par-cles.md)
- [4.4 — Durcissement de `sshd_config`](campagne_04/4.4-durcissement-sshd-config.md)
- [4.5 — Bastion d'administration](campagne_04/4.5-bastion-administration.md)
- [4.6 — Journalisation et audit SSH](campagne_04/4.6-journalisation-audit-ssh.md)
- [4.7 — Protection contre les attaques SSH](campagne_04/4.7-protection-attaques-ssh.md)
- [4.8 — Mission : administrer Sentinel en sécurité](campagne_04/4.8-mission-administration-sentinel.md)

### Campagne 5 — systemd et services

- [5.1 — Comprendre `systemd`](campagne_05/5.1-comprendre-systemd.md)
- [5.2 — Les unités `systemd`](campagne_05/5.2-unites-systemd.md)
- [5.3 — Créer le service Sentinel](campagne_05/5.3-creer-service-sentinel.md)
- [5.4 — Sandboxing `systemd`](campagne_05/5.4-sandboxing-systemd.md)
- [5.5 — Les capacités Linux](campagne_05/5.5-capacites-linux.md)
- [5.6 — Journalisation avec `journald`](campagne_05/5.6-journalisation-journald.md)
- [5.7 — Supervision et redémarrage automatique](campagne_05/5.7-supervision-redemarrage.md)
- [5.8 — Mission : rendre Sentinel résilient](campagne_05/5.8-mission-sentinel-resilient.md)

### Campagne 6 — SELinux

- [6.1 — Pourquoi SELinux existe](campagne_06/6.1-pourquoi-selinux-existe.md)
- [6.2 — Les contextes SELinux](campagne_06/6.2-contextes-selinux.md)
- [6.3 — Les politiques SELinux](campagne_06/6.3-politiques-selinux.md)
- [6.4 — Diagnostic des refus SELinux](campagne_06/6.4-diagnostic-refus-selinux.md)
- [6.5 — Création de règles SELinux](campagne_06/6.5-creation-regles-selinux.md)
- [6.6 — Sécuriser Sentinel avec SELinux](campagne_06/6.6-securiser-sentinel-selinux.md)

### Campagne 7 — TLS et PKI

- [7.1 — Comprendre la cryptographie appliquée](campagne_07/7.1-comprendre-cryptographie-appliquee.md)
- [7.2 — Lire et vérifier les certificats X.509](campagne_07/7.2-lire-verifier-certificats-x509.md)
- [7.3 — Construire une autorité de certification](campagne_07/7.3-construire-autorite-certification.md)
- [7.4 — Authentifier les deux extrémités avec mTLS](campagne_07/7.4-authentification-mutuelle-tls.md)
- [7.5 — Préparer l'intégration à FreeIPA](campagne_07/7.5-preparer-integration-freeipa.md)
- [7.6 — Renouveler et révoquer les certificats](campagne_07/7.6-renouveler-revoquer-certificats.md)
- [7.7 — Sécuriser Sentinel avec TLS](campagne_07/7.7-securiser-sentinel-tls.md)

## Partie II — Industrialiser la sécurité

### Campagne 8 — FreeIPA

- [8.1 — Découvrir FreeIPA et la gestion centralisée des identités](campagne_08/8.1-presentation-freeipa.md)
- [8.2 — Comprendre l'architecture interne de FreeIPA](campagne_08/8.2-architecture-interne-freeipa.md)
- [8.3 — Installer un serveur FreeIPA de laboratoire](campagne_08/8.3-installation-freeipa.md)
- [8.4 — Gérer le cycle de vie des utilisateurs FreeIPA](campagne_08/8.4-gestion-utilisateurs.md)
- [8.5 — Organiser les groupes et les rôles FreeIPA](campagne_08/8.5-groupes-roles.md)
- [8.6 — Centraliser les politiques `sudo` avec FreeIPA](campagne_08/8.6-politiques-sudo.md)
- [8.7 — Enrôler les hôtes et contrôler les accès avec HBAC](campagne_08/8.7-gestion-hotes.md)
- [8.8 — Gérer les certificats de service avec FreeIPA](campagne_08/8.8-certificats.md)
- [8.9 — Intégrer Sentinel à FreeIPA](campagne_08/8.9-integration-sentinel.md)
- [8.10 — Mission : administrer Sentinel avec FreeIPA](campagne_08/8.10-mission-administration-freeipa.md)

### Campagne 9 — Déploiement avec Ansible

- [9.1 — Comprendre l'architecture Ansible](campagne_09/9.1-architecture-ansible.md)
- [9.2 — Comprendre les composants et l'idempotence Ansible](campagne_09/9.2-composants-ansible.md)
- [9.3 — Construire les inventaires Ansible](campagne_09/9.3-inventaires.md)
- [9.4 — Écrire les premiers playbooks](campagne_09/9.4-premiers-playbooks.md)
- [9.5 — Piloter la configuration avec variables et templates](campagne_09/9.5-variables-templates.md)
- [9.6 — Concevoir des rôles Ansible réutilisables](campagne_09/9.6-roles-ansible.md)
- [9.7 — Déployer Sentinel avec Ansible](campagne_09/9.7-deployer-sentinel-ansible.md)
- [9.8 — Automatiser l'intégration de Sentinel à FreeIPA](campagne_09/9.8-integrer-sentinel-freeipa.md)
- [9.9 — Industrialiser le projet Ansible](campagne_09/9.9-industrialiser-laboratoire.md)
- [9.10 — Mission : reconstruire Sentinel avec Ansible](campagne_09/9.10-mission-deploiement-sentinel.md)

### Campagne 10 — RPM et cycle de vie

- [10.1 — Construire un paquet RPM](campagne_10/10.1-construire-paquet-rpm.md)
- [10.2 — Gérer les dépendances RPM](campagne_10/10.2-gerer-dependances-rpm.md)
- [10.3 — Gérer les fichiers de configuration RPM](campagne_10/10.3-gerer-fichiers-configuration-rpm.md)
- [10.4 — Signer les paquets RPM](campagne_10/10.4-signer-paquets-rpm.md)
- [10.5 — Exploiter un dépôt RPM privé](campagne_10/10.5-exploiter-depot-rpm-prive.md)
- [10.6 — Packager Sentinel](campagne_10/10.6-packager-sentinel.md)

### Campagne 11 — Conteneurisation

- [11.1 — Découvrir Podman](campagne_11/11.1-decouvrir-podman.md)
- [11.2 — Exécuter des conteneurs rootless](campagne_11/11.2-conteneurs-rootless.md)
- [11.3 — Construire des images sécurisées](campagne_11/11.3-construire-images-securisees.md)
- [11.4 — Concevoir les réseaux de conteneurs](campagne_11/11.4-reseaux-conteneurs.md)
- [11.5 — Gérer les secrets avec Podman](campagne_11/11.5-gerer-secrets-podman.md)
- [11.6 — Exécuter Sentinel en sécurité](campagne_11/11.6-executer-sentinel-securite.md)

### Campagne 12 — Supervision et audit

- [12.1 — Centraliser les journaux avec Rsyslog](campagne_12/12.1-centraliser-journaux-rsyslog.md)
- [12.2 — Auditer le système avec `auditd`](campagne_12/12.2-auditer-systeme-auditd.md)
- [12.3 — Contrôler l'intégrité des fichiers avec AIDE](campagne_12/12.3-controler-integrite-fichiers-aide.md)
- [12.4 — Superviser Sentinel avec Prometheus](campagne_12/12.4-superviser-sentinel-prometheus.md)
- [12.5 — Concevoir des alertes avec Alertmanager](campagne_12/12.5-concevoir-alertes-alertmanager.md)
- [12.6 — Construire le tableau de bord Sentinel](campagne_12/12.6-construire-tableau-bord-sentinel.md)

## Partie III — Mise en situation

### Campagne 13 — Attaques et défense

La campagne suit un cycle commun : observer, produire un événement contrôlé, collecter les traces, corriger puis retester.

- [13.1 — Reconnaissance](campagne_13/13.1-reconnaissance.md)
- [13.2 — Scan réseau](campagne_13/13.2-scan-reseau.md)
- [13.3 — Brute force SSH](campagne_13/13.3-brute-force-ssh.md)
- [13.4 — Escalade de privilèges](campagne_13/13.4-escalade-privileges.md)
- [13.5 — Mouvements latéraux](campagne_13/13.5-mouvements-lateraux.md)
- [13.6 — Persistance](campagne_13/13.6-persistance.md)
- [13.7 — Exfiltration](campagne_13/13.7-exfiltration.md)
- [13.8 — Étude de cas complète](campagne_13/13.8-etude-cas-complete.md)

### Campagne 14 — Projet final

- [14.1 — Déployer Sentinel sur une AlmaLinux minimale](campagne_14/14.1-deployer-sentinel-almalinux-minimale.md)
- [14.2 — Sécuriser l'hôte](campagne_14/14.2-securiser-hote.md)
- [14.3 — Intégrer FreeIPA](campagne_14/14.3-integrer-freeipa.md)
- [14.4 — Déployer avec Ansible](campagne_14/14.4-deployer-ansible.md)
- [14.5 — Packager avec RPM](campagne_14/14.5-packager-rpm.md)
- [14.6 — Conteneuriser avec Podman](campagne_14/14.6-conteneuriser-podman.md)
- [14.7 — Superviser et auditer](campagne_14/14.7-superviser-auditer.md)
- [14.8 — Audit final et tests depuis Kali](campagne_14/14.8-audit-final-tests-kali.md)
