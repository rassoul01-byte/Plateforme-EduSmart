# Phase 14 — Data Storytelling

## Objectif
Apprendre à raconter une histoire à partir des données, pour convaincre un décideur plutôt que simplement lui montrer des chiffres.

## Recherche

**Qu'est-ce que le Data Storytelling ?**
Le Data Storytelling est l'art de structurer une analyse de données comme un récit avec un début, un développement et une conclusion, plutôt que comme une simple liste de chiffres. Il combine trois éléments : les données elles-mêmes, la visualisation, et la narration qui donne du sens aux deux premiers.

**Comment raconter une histoire avec les données ?**
En partant d'un contexte clair (pourquoi ce sujet compte), en présentant une tension ou une question (qu'observe-t-on d'inattendu ou de préoccupant ?), puis en amenant progressivement vers un insight et une recommandation actionnable, plutôt que d'aligner des graphiques sans fil conducteur.

**Comment convaincre un décideur ?**
En allant à l'essentiel (un décideur n'a pas le temps de lire 20 graphiques), en anticipant ses questions plutôt qu'en attendant qu'il les pose, en reliant chaque chiffre à une décision concrète possible, et en terminant toujours par une recommandation claire plutôt que par un simple constat.

## TP — Présentation des résultats EduSmart

**Contexte** : EduSmart dispose de cinq sources de données disparates (académique, pédagogique, RH, logs mobile, temps réel), rendant impossible une vue consolidée pour la direction.

### Ce qu'on a découvert en consolidant les données

1. Le chiffre d'affaires total s'élève à 5,23 milliards, avec un pic marqué en 2025 suivi d'une baisse en 2026, un signal qui mérite d'être creusé (nouvelle concurrence, saisonnalité, ou année 2026 simplement incomplète dans les données actuelles).
2. Le taux de réussite global se situe à 50,83%, soit un étudiant sur deux qui obtient une note supérieure ou égale à 10/20, un chiffre qui interroge sur la qualité pédagogique ou le niveau de difficulté des évaluations.
3. Le chiffre d'affaires se répartit de façon inégale entre les villes couvertes (Dakar, Thiès, Mbour, Kaolack, Rufisque, Diourbel, Saint-Louis), révélant des marchés régionaux à des stades de maturité différents.

### Recommandation proposée

Prioriser une investigation sur la baisse de 2026 avant qu'elle ne s'aggrave, et lancer une analyse ciblée du taux de réussite par formation (déjà identifié comme KPI en Phase 11) pour identifier les cours qui tirent la moyenne vers le bas. Ces deux actions s'appuient directement sur le Data Warehouse et les visuels construits en Phase 13, sans nécessiter de nouvelle collecte de données.

### Fil conducteur retenu pour la présentation finale (Phase 18)

Partir du problème initial (données éclatées, décisions à l'aveugle), montrer le chemin parcouru (ETL, qualité, Data Warehouse, modélisation), puis terminer sur ce que ces données révèlent concrètement et ce que la direction devrait décider en conséquence.