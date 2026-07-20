# Sentinel 0.1.0

Ce checkpoint correspond à la fin de la campagne 1.

Fonctions disponibles :

- affichage de la version ;
- diagnostic local de l'hôte ;
- sortie lisible ou JSON ;
- codes de retour prévisibles ;
- tests avec la bibliothèque standard Python.

Exécution :

```bash
python3 src/sentinel.py --version
python3 src/sentinel.py status
python3 src/sentinel.py status --format json
python3 -m unittest discover -s tests -v
```

Cette version n'écoute sur aucun port, n'écrit aucun état persistant et ne nécessite aucun privilège administratif.
