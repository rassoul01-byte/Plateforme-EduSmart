# Phase 12 — Analyse et Visualisation des Données

## Objectif
Choisir, pour chaque KPI défini en Phase 11, le type de visualisation le plus adapté, et être capable de justifier ce choix.

## Rappel des types de visualisations connus

Histogramme, boxplot, scatterplot, heatmap, barplot, auxquels s'ajoutent, dans une logique de tableau de bord décisionnel, la courbe (line chart), la carte KPI (single value card), et le classement (ranked bar/table).

## TP — Choix des visualisations pour EduSmart

| KPI | Visualisation choisie | Pourquoi ce choix | Pourquoi pas un autre |
|---|---|---|---|
| Chiffre d'affaires (total) | Carte KPI (valeur unique) | Le DG veut un chiffre immédiat, sans effort de lecture, pour une vue d'ensemble instantanée. | Un barplot serait inutile pour une seule valeur, il ajoute du bruit visuel sans apporter d'information supplémentaire. |
| Chiffre d'affaires dans le temps | Courbe (line chart) | La dimension temporelle et la tendance (croissance, saisonnalité) sont l'information recherchée, pas des valeurs isolées. | Un barplot fonctionnerait aussi, mais la courbe rend les variations et la tendance générale plus lisibles sur de nombreuses périodes. |
| Chiffre d'affaires par ville | Barplot (barres horizontales) | Comparer des catégories distinctes (villes) entre elles, cas d'usage classique du barplot. | Un scatterplot n'a pas de sens ici : il n'y a pas de relation entre deux variables continues, juste une comparaison catégorielle. |
| Taux de réussite par formation | Barplot avec ligne de seuil | Permet de comparer rapidement les formations à un seuil de référence, avec un repère visuel clair. | Une heatmap serait excessive pour une seule dimension (formation) ; elle est plus utile pour croiser deux dimensions. |
| Distribution des notes | Boxplot | Montre la médiane, la dispersion et les valeurs extrêmes en un coup d'œil, utile pour repérer des anomalies. | Un histogramme donnerait la forme de la distribution mais serait moins efficace pour comparer plusieurs formations côte à côte. |
| Taux d'abandon | Carte KPI + courbe d'évolution | Un chiffre choc immédiat, complété par une tendance pour voir si la situation s'aggrave ou s'améliore. | Un scatterplot ne conviendrait pas : le taux d'abandon est une métrique agrégée dans le temps, pas une relation entre deux variables individuelles. |
| Progression moyenne vs temps de connexion | Scatterplot | Explore une relation possible entre deux variables continues (plus de temps connecté implique-t-il plus de progression ?). | Un barplot masquerait la relation entre les deux variables continues, qui est justement ce qu'on cherche à visualiser. |
| Activité par ville et par mois | Heatmap | Croise deux dimensions catégorielles (ville x mois) avec une intensité de couleur, idéal pour repérer des pics ou creux d'activité régionaux. | Un barplot empilé deviendrait illisible avec autant de villes et de mois combinés. |
| Enseignants les mieux évalués | Classement (ranked barplot, Top 10) | Répond directement à la question "qui sont les meilleurs ?" avec un ordre visuel clair. | Un scatterplot ou une heatmap ajouteraient de la complexité inutile pour ce qui est fondamentalement une liste ordonnée. |
| Nombre d'étudiants actifs dans le temps | Courbe (line chart) | Suivre l'évolution de l'engagement global, avec la possibilité de repérer des baisses saisonnières. | Une carte seule perdrait l'information de tendance, essentielle pour ce KPI d'engagement. |

## Principe général retenu

Le choix ne dépend jamais du graphique le plus impressionnant visuellement, mais de la nature de la question posée : une valeur unique appelle une carte, une évolution appelle une courbe, une comparaison entre catégories appelle un barplot, une distribution appelle un boxplot ou un histogramme, une relation entre deux variables continues appelle un scatterplot, et un croisement de deux dimensions catégorielles appelle une heatmap.

## Prochaine étape

Ces choix de visualisation guideront directement la construction du tableau de bord Power BI (Phase 13), où chaque KPI sera représenté par le visuel identifié ici.