# Sentinel 0.2.0

Ce checkpoint correspond à la fin de la campagne 2. Il conserve les commandes de la version 0.1.0 et ajoute une configuration validable ainsi qu'un état persistant.

```bash
python3 src/sentinel.py --version
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 src/sentinel.py --config config/sentinel.conf record
python3 src/sentinel.py --config config/sentinel.conf show --format json
python3 -m unittest discover -s tests -v
```

Le fichier d'état est écrit de manière atomique avec le mode `0640`. Les permissions du répertoire restent une responsabilité de l'administrateur : les tests de campagne doivent démontrer les accès autorisés et refusés sous les identités prévues.
