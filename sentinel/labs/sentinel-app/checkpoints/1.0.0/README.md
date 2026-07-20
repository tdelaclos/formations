# Sentinel 1.0.0

Ce checkpoint correspond à la fin de la campagne 10. Les interfaces qualifiées de 0.6.0 sont stabilisées et accompagnées des fichiers nécessaires au paquet RPM.

Nouveautés :

- code installé sous `/usr/libexec/sentinel/` ;
- configuration sous `/etc/sentinel/sentinel.conf` ;
- unité systemd compatible avec `Type=notify` et le watchdog ;
- état créé par `StateDirectory=sentinel` ;
- mêmes contrats CLI, HTTP, mTLS et identité que la version qualifiée.

```bash
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf serve
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf --healthcheck
python3 -m unittest discover -s tests -v
```

La recette complète et les commandes de qualification restent expliquées au chapitre 10.6. Le checkpoint ne contient aucune clé privée ni RPM construit.
