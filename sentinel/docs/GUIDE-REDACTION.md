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

> *« Citation éventuelle. »*

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

## Schéma récapitulatif

Illustration éventuelle lorsqu'une image récapitulative pertinente existe déjà dans `media/`.

## Pour aller plus loin

Transition éventuelle vers le chapitre suivant.
```

Les trois premières sections de niveau 2 sont donc toujours, dans cet ordre : **Vous êtes ici**, **Objectifs pédagogiques**, puis **Pourquoi ce chapitre existe**. Le cartouche situé entre le titre et **Vous êtes ici** conserve le nom de la campagne et, lorsqu'elle existe, la citation du chapitre.

Les chapitres de mission conservent cette ossature. Leur corps peut toutefois être organisé en contexte, contraintes, travail demandé, critères de réussite et livrables.

La section **Schéma récapitulatif** est facultative. Elle sert uniquement à afficher une illustration de synthèse réellement disponible ; elle ne doit pas conduire à fabriquer artificiellement une image pour chaque chapitre.

## Jalons de l'application Sentinel

Lorsqu'un chapitre modifie concrètement l'application fil rouge, il ajoute une section `Jalon Sentinel`. Cette section précise :

- la version de départ et les fonctions déjà acquises ;
- le besoin opérationnel introduit par la campagne ;
- les fichiers et interfaces modifiés ;
- la compatibilité de la configuration et des données ;
- les tests automatisés et fonctionnels ;
- au moins un échec, refus ou scénario de panne attendu ;
- le commit ou la version qui devient l'entrée du jalon suivant.

Une campagne peut appliquer un mécanisme à Sentinel sans modifier le code. Dans ce cas, elle conserve la version applicative et versionne séparément la configuration ou l'infrastructure. La trajectoire commune et les interfaces déjà acquises sont définies dans le [parcours applicatif Sentinel](PARCOURS-SENTINEL.md).

Les extraits proposés doivent être exécutables ou indiquer sans ambiguïté le fichier et le point d'insertion. Un chapitre ne doit pas supposer l'existence d'une option CLI, d'une route HTTP, d'un chemin ou d'une métrique qui n'a pas été introduit dans un jalon antérieur.

## Hiérarchie des titres

- un seul titre de niveau 1 (`#`) : le titre du chapitre ;
- les grandes sections utilisent le niveau 2 (`##`) ;
- leurs subdivisions utilisent le niveau 3 (`###`) ;
- les détails internes utilisent les niveaux 4 à 6 si nécessaire ;
- les niveaux ne doivent pas être choisis pour leur apparence visuelle.

## Diagrammes

Les représentations conceptuelles et les flux utilisent Mermaid lorsque le diagramme apporte une information plus claire que le texte seul. Le type de diagramme doit correspondre au message :

- `flowchart` pour une chaîne de traitement, une architecture ou plusieurs relations ;
- `sequenceDiagram` pour des échanges entre composants ;
- `stateDiagram-v2` pour un cycle de vie ;
- `classDiagram`, `mindmap`, `timeline` ou d'autres syntaxes Mermaid lorsqu'elles sont plus pertinentes.

Un diagramme n'est pas ajouté uniquement pour illustrer deux mots ou une relation triviale déjà expliquée par la phrase qui l'entoure. Dans un chapitre riche en schémas, privilégier quelques représentations structurantes plutôt qu'une succession de micro-flowcharts.

La table des matières placée dans **Vous êtes ici** reste volontairement textuelle. Les sorties de commandes, arborescences de fichiers, configurations et extraits de journaux ne sont pas des diagrammes : ils restent dans des blocs de code adaptés.

## Images récapitulatives

Lorsqu'une image pédagogique existe dans le répertoire `media/` de la campagne, elle est intégrée avec du Markdown standard afin d'être rendue aussi bien par GitHub que par MkDocs :

```markdown
## Schéma récapitulatif

![Récapitulatif visuel du chapitre X.Y](media/recap-X.Y.png)
```

Règles associées :

- utiliser un chemin relatif au fichier du chapitre ;
- fournir un texte alternatif qui décrit la fonction de l'image ;
- ne jamais dépendre uniquement d'une couleur pour transmettre une information ;
- ne pas dupliquer sous forme ASCII une image déjà affichée ;
- conserver dans le texte les informations indispensables à la compréhension et aux exercices.

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
- les trois sections introductives sont présentes et dans le même ordre ;
- une section **Synthèse** est présente ;
- chaque Mermaid apporte une relation, une architecture, une séquence ou un état utile ;
- les diagrammes Mermaid possèdent des clôtures de blocs correctes ;
- les liens vers les chapitres précédent et suivant pointent vers des fichiers existants ;
- les images référencées existent dans le répertoire `media/` de la campagne ;
- le rendu MkDocs est construit sans erreur avant publication.
