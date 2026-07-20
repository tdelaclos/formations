# Sentinel 1.1.0

Ce checkpoint correspond à la campagne 12. Il conserve les interfaces et le packaging 1.0.0, puis ajoute un endpoint Prometheus réellement alimenté par les requêtes HTTP.

Nouveautés :

- `sentinel_build_info{version,revision}` ;
- compteur des requêtes par route normalisée et code ;
- jauge des requêtes en cours ;
- histogramme de durée ;
- état de la dépendance locale et date du dernier diagnostic réussi.

```bash
python3 src/sentinel.py --config config/sentinel.conf --check-config
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf serve
python3 src/sentinel.py --config /etc/sentinel/sentinel.conf --healthcheck
python3 -m unittest discover -s tests -v
```

La version 1.0.0 reste celle de l'image construite pendant la campagne 11 : la conteneurisation n'avait exigé aucun changement de code. La version 1.1.0 est créée seulement lorsque le contrat applicatif évolue avec `/metrics`.
