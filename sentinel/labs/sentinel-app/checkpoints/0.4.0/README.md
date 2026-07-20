# Sentinel 0.4.0

Ce checkpoint correspond à la fin de la campagne 5. L'interface HTTP devient un processus exploitable par systemd.

Nouveautés :

- route `/ready` distincte de `/health` ;
- option `--healthcheck` utilisable par une unité ou un conteneur ;
- arrêt propre sur `SIGTERM` et `SIGINT` ;
- notifications `READY=1`, `WATCHDOG=1` et `STOPPING=1` lorsque `NOTIFY_SOCKET` existe ;
- journaux JSON sur la sortie standard.

```bash
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 src/sentinel.py --config config/sentinel.conf serve
python3 src/sentinel.py --config config/sentinel.conf --healthcheck
python3 -m unittest discover -s tests -v
```
