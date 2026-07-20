# Application de référence Sentinel

Ce répertoire contient les jalons exécutables de l'application fil rouge. Il complète les chapitres sans remplacer le travail demandé à l'apprenant.

Chaque répertoire sous `checkpoints/` représente un état accepté du produit. Un checkpoint comprend le code, les tests et les métadonnées nécessaires pour reprendre la formation au début du jalon suivant.

Règles de maintenance :

- un checkpoint déjà publié reste reproductible ;
- une correction rétroactive est documentée dans son README ;
- les interfaces acquises sont conservées dans les versions suivantes ;
- aucun secret, état d'exécution ou artefact construit n'est enregistré ici ;
- le code reste volontairement petit afin que les mécanismes Linux demeurent le sujet principal.

Le premier checkpoint, `0.1.0`, est construit au chapitre 1.10.
