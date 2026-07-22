# Laboratoire Ansible de Sentinel

Ce projet accompagne la campagne 9. Il déploie le checkpoint Sentinel `0.6.0` sans modifier son code, puis prépare son intégration au domaine FreeIPA de la campagne 8.

## Préconditions

- un nœud de contrôle avec `ansible-core` ;
- les FQDN du laboratoire résolus ;
- un compte `ansible` accessible par clé SSH et autorisé par une politique `sudo` contrôlée ;
- le domaine `SENTINEL.EXAMPLE.TEST` disponible pour le playbook d'enrôlement ;
- les protections systemd, SELinux et Firewalld des campagnes précédentes.

## Préparer le projet

```bash
cd sentinel/labs/ansible
ansible-galaxy collection install -r requirements.yml
ansible --version
ansible-config dump --only-changed
ansible-inventory --graph
```

Adaptez les adresses de `inventories/lab/hosts.yml` au réseau isolé. Vérifiez les clés SSH des hôtes au lieu de désactiver `host_key_checking`.

## Secret FreeIPA

Copiez uniquement la structure de l'exemple puis chiffrez le vrai fichier :

```bash
install -d inventories/lab/group_vars/ipaclients
cp inventories/lab/group_vars/ipaclients/vault.example.yml \
  inventories/lab/group_vars/ipaclients/vault.yml
ansible-vault encrypt inventories/lab/group_vars/ipaclients/vault.yml
```

Ne conservez pas la valeur `CHANGE_ME_WITH_A_SECRET_SOURCE`. Le secret Vault ou son mot de passe ne doit pas entrer dans Git.

## Vérifier et exécuter

```bash
ansible-playbook playbooks/site.yml --syntax-check
ansible-playbook playbooks/site.yml --list-hosts
ansible-playbook playbooks/deploy-sentinel.yml \
  --limit sentinel01.sentinel.example.test
ansible-playbook playbooks/verify.yml \
  --limit sentinel01.sentinel.example.test
```

Le premier déploiement conserve TLS désactivé. Le chapitre 9.8 enrôle les hôtes, obtient localement les certificats avec `certmonger`, puis active les variables mTLS.

Relancez chaque playbook sans changer ses entrées. Le second passage complet doit produire `changed=0`.
