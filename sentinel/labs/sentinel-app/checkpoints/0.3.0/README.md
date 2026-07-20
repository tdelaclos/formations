# Sentinel 0.3.0

Ce checkpoint correspond à la fin de la campagne 3. Sentinel devient un service HTTP réel afin que les exercices réseau portent sur un processus observable.

```bash
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 src/sentinel.py --config config/sentinel.conf record
python3 src/sentinel.py --config config/sentinel.conf serve
curl --fail http://127.0.0.1:8443/health
curl --fail http://127.0.0.1:8443/api/v1/status
python3 -m unittest discover -s tests -v
```

L'adresse d'écoute reste locale dans la configuration fournie. L'exposition sur une interface du laboratoire doit être explicite et accompagnée de la politique Firewalld correspondante.
