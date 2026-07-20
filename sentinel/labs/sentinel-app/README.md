# Application de référence Sentinel

Ce répertoire contient les jalons exécutables de l'application fil rouge. Il complète les chapitres sans remplacer le travail demandé à l'apprenant.

Chaque répertoire sous `checkpoints/` représente un état accepté du produit. Un checkpoint comprend le code, les tests et les métadonnées nécessaires pour reprendre la formation au début du jalon suivant.

À partir de `0.2.0`, `src/sentinel.py` est seulement le point d'entrée stable. Le code est réparti en modules nommés par responsabilité. Chaque module possède une docstring qui indique la campagne ayant introduit la notion ; les commentaires expliquent les décisions de sécurité ou d'exploitation, pas la syntaxe Python évidente.

Règles de maintenance :

- un checkpoint déjà publié reste reproductible ;
- une correction rétroactive est documentée dans son README ;
- les interfaces acquises sont conservées dans les versions suivantes ;
- aucun secret, état d'exécution ou artefact construit n'est enregistré ici ;
- le code reste volontairement petit afin que les mécanismes Linux demeurent le sujet principal.

| Checkpoint | Construction | Fonction principale |
| --- | --- | --- |
| `0.1.0` | chapitre 1.10 | diagnostic local et contrat CLI |
| `0.2.0` | chapitre 2.10 | configuration et état persistant |
| `0.3.0` | chapitre 3.10 | interface HTTP réelle |
| `0.4.0` | chapitre 5.8 | service compatible avec systemd |
| `0.5.0` | campagne 7 | TLS et authentification mutuelle |
| `0.6.0` | chapitre 8.9 | autorisation des identités de certificat |
| `1.0.0` | chapitre 10.6 | interfaces stabilisées et fichiers RPM |
| `1.1.0` | chapitre 12.4 | métriques Prometheus réelles |

La campagne 4 administre le checkpoint 0.3.0 sans changer son code. La campagne 6 confine le checkpoint 0.4.0 et versionne séparément la politique SELinux.
La campagne 9 déploie 0.6.0 sans modification. La campagne 11 construit une image de 1.0.0 et versionne l'image par son digest sans créer une version applicative artificielle.
