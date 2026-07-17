# Guide de rédaction des chapitres

Ce document définit le formalisme commun des campagnes de la formation Sentinel. Il doit être appliqué à tout nouveau chapitre et conservé lors des révisions.

## Convention de nommage

Un fichier de chapitre suit la forme :

```text
<campagne>.<chapitre>-<sujet-en-kebab-case>.md
```

Exemples :

```text
4.1-architecture-openssh.md
6.4-diagnostic-refus-selinux.md
9.7-deployer-sentinel-ansible.md
```

Le numéro conserve le lien avec le plan de formation. Le sujet rend le fichier identifiable sans devoir l'ouvrir. Les noms utilisent exclusivement des caractères ASCII minuscules, des chiffres, des points et des traits d'union.

## Structure obligatoire

Chaque chapitre respecte l'ordre général suivant :

```markdown
# Chapitre X.Y — Titre explicite

> **Campagne X — Nom de la campagne**

## Vous êtes ici

Table des matières textuelle de la campagne.

## Objectifs pédagogiques

- objectif observable 1 ;
- objectif observable 2 ;
- objectif observable 3.

## Pourquoi ce chapitre existe

Contexte, problème traité et lien avec Sentinel.

## Sections pédagogiques

Théorie, démonstrations, points d'expertise et mises en pratique.

## Synthèse

Notions et compétences à retenir.

## Infographie de révision

Infographie finale éventuelle.

## Pour aller plus loin

Transition éventuelle vers le chapitre suivant.
```

Les chapitres de mission conservent cette ossature. Leur corps peut toutefois être organisé en contexte, contraintes, travail demandé, critères de réussite et livrables.

## Hiérarchie des titres

- un seul titre de niveau 1 (`#`) : le titre du chapitre ;
- les grandes sections utilisent le niveau 2 (`##`) ;
- leurs subdivisions utilisent le niveau 3 (`###`) ;
- les détails internes utilisent les niveaux 4 à 6 si nécessaire ;
- les niveaux ne doivent pas être choisis pour leur apparence visuelle.

## Diagrammes

Les représentations conceptuelles et les flux utilisent Mermaid. Le type de diagramme doit correspondre au message :

- `flowchart` pour une chaîne de traitement ou une architecture ;
- `sequenceDiagram` pour des échanges entre composants ;
- `stateDiagram-v2` pour un cycle de vie ;
- `classDiagram`, `mindmap`, `timeline` ou d'autres syntaxes Mermaid lorsqu'elles sont plus pertinentes.

Deux exceptions restent volontairement textuelles ou graphiques :

1. la table des matières placée dans **Vous êtes ici** ;
2. l'infographie récapitulative placée en fin de chapitre.

Les sorties de commandes, arborescences de fichiers, configurations et extraits de journaux ne sont pas des diagrammes : ils restent dans des blocs de code adaptés.

## Règles éditoriales

- conserver un vocabulaire cohérent d'un chapitre à l'autre ;
- introduire un terme avant de l'utiliser dans un exercice ;
- relier les notions au laboratoire Sentinel lorsque cela apporte une application concrète ;
- distinguer clairement théorie, commande exécutée, résultat attendu et interprétation ;
- éviter les répétitions décoratives et les séparateurs successifs ;
- terminer par une synthèse vérifiable plutôt que par une simple formule de clôture.

## Contrôles avant publication

- le titre et le nom du fichier décrivent le même sujet ;
- un seul titre de niveau 1 existe hors des blocs de code ;
- les trois sections introductives sont présentes ;
- une section **Synthèse** est présente ;
- les diagrammes Mermaid possèdent des clôtures de blocs correctes ;
- les liens vers les chapitres précédent et suivant pointent vers des fichiers existants ;
- les images référencées existent dans le répertoire `media/` de la campagne.
