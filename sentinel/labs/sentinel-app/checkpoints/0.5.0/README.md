# Sentinel 0.5.0

Ce checkpoint constitue le jalon TLS attendu à la fin de la campagne 7. Il conserve les propriétés systemd de 0.4.0 et peut protéger l'interface HTTP par TLS ou mTLS.

Nouveautés :

- contexte TLS serveur construit depuis la configuration ;
- validation de la chaîne cliente par une autorité approuvée ;
- certificat client distinct pour le healthcheck local ;
- refus d'un pair sans certificat lorsque le mTLS est obligatoire.

```bash
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf serve
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf --healthcheck
python3 -m unittest discover -s tests -v
```

La configuration fournie garde TLS désactivé afin de rester exécutable sans clé privée dans Git. Le chapitre TLS crée les certificats dans le laboratoire, active les options et prouve les connexions acceptées et refusées.
