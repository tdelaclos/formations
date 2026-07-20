# Sentinel 1.0.0

Ce checkpoint correspond à la fin de la campagne 10. Les interfaces qualifiées de 0.6.0 sont stabilisées et accompagnées des fichiers nécessaires au paquet RPM.

Nouveautés :

- code installé sous `/usr/libexec/sentinel/` ;
- configuration sous `/etc/sentinel/sentinel.conf` ;
- unité systemd compatible avec `Type=notify` et le watchdog ;
- état créé par `StateDirectory=sentinel` ;
- mêmes contrats CLI, HTTP, mTLS et identité que la version qualifiée.

## Organisation du code

Le lanceur `src/sentinel.py` reste installé comme `/usr/libexec/sentinel/sentinel`. Les modules Python voisins sont installés dans le même répertoire : la stabilisation `1.0.0` porte donc sur tout le graphe de modules, pas seulement sur le lanceur. Le sous-répertoire `packaging/` conserve la configuration et l'unité systemd.

```bash
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf serve
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf --healthcheck
python3 -m unittest discover -s tests -v
```

La recette complète et les commandes de qualification restent expliquées au chapitre 10.6. Le checkpoint ne contient aucune clé privée ni RPM construit.
