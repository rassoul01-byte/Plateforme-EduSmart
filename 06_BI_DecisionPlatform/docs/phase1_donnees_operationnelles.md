# Phase 1 — De la donnée opérationnelle à la décision

## Objectif
Comprendre pourquoi les entreprises mettent en place des systèmes décisionnels.

## Partie A — Comprendre les données opérationnelles

**1. Qu'appelle-t-on une donnée opérationnelle ?**
Une donnée opérationnelle est une donnée produite et utilisée au quotidien par les systèmes qui font fonctionner l'entreprise : une inscription d'étudiant, un paiement, une connexion au LMS, une note de quiz. Elle décrit un événement précis, à un instant donné, et sert avant tout à faire tourner l'activité (pas à l'analyser).

**2. Qu'est-ce qu'une base OLTP ?**
OLTP (*OnLine Transaction Processing*) désigne une base de données conçue pour traiter un grand nombre de transactions courtes et fréquentes (insert/update/delete) en temps réel — typiquement PostgreSQL ou MySQL dans EduSmart. Elle est optimisée pour l'écriture rapide et l'intégrité des données, pas pour l'analyse de gros volumes.

**3. Pourquoi une entreprise possède-t-elle plusieurs bases de données ?**
Parce que chaque activité métier a des besoins différents : gestion académique, pédagogie en ligne, RH, temps réel. Utiliser une base unique pour tout créerait un goulot d'étranglement et un couplage risqué entre systèmes qui évoluent à des rythmes différents.

**4. Pourquoi chaque service possède-t-il souvent son propre système d'information ?**
Chaque service (académique, pédagogique, RH) a des processus, des contraintes techniques et des rythmes de mise à jour propres. Un système dédié permet de choisir la technologie la mieux adaptée (SQL, NoSQL, cache temps réel) et de faire évoluer chaque service indépendamment.

**5. Quels sont les avantages de cette organisation ?**
Performance (chaque base est optimisée pour son usage), autonomie des équipes, résilience (une panne reste isolée), et flexibilité technologique (on choisit le bon outil pour chaque besoin : Redis pour le temps réel, MongoDB pour les logs, etc.).

## Partie B — Les limites des systèmes opérationnels

**6. Quels problèmes rencontre-t-on lorsque les données sont réparties dans plusieurs systèmes ?**
Absence de vue globale, difficulté à croiser les informations, risque d'incohérence entre systèmes, duplication des efforts pour obtenir un chiffre consolidé, et lenteur pour répondre à une question transversale.

**7. Pourquoi les identifiants peuvent-ils être différents d'une base à l'autre ?**
Chaque système a été conçu indépendamment, avec ses propres règles de génération d'ID (auto-incrément PostgreSQL, ObjectId MongoDB, clé Redis). Un même étudiant peut donc avoir un identifiant différent dans chaque source, ce qui complique le rapprochement des données.

**8. Pourquoi une même information peut-elle être présente plusieurs fois ?**
Parce que certains attributs (nom, email d'un étudiant par exemple) sont dupliqués dans plusieurs systèmes pour que chacun fonctionne de façon autonome, sans dépendre en temps réel des autres.

**9. Quels risques cela représente-t-il pour les décideurs ?**
Des chiffres contradictoires selon la source consultée, une perte de confiance dans les données, des décisions prises sur des informations incomplètes ou obsolètes.

## Partie C — Les besoins métier

**10. Quelles informations un Directeur Général souhaite-t-il consulter quotidiennement ?**
Des indicateurs de synthèse : chiffre d'affaires, nombre d'étudiants actifs, taux de réussite, satisfaction, performance des formations — des informations agrégées, pas des lignes brutes de transactions.

**11. Ces informations existent-elles dans une seule base ?**
Non — elles nécessitent de croiser plusieurs sources (paiements en PostgreSQL, notes/connexions en MySQL, logs mobile en JSON/MongoDB, sessions temps réel en Redis).

**12. Pourquoi un directeur ne consulte-t-il jamais directement les bases opérationnelles ?**
Parce que ces bases sont techniques, fragmentées, changent en permanence, et une requête lourde d'analyse pourrait ralentir le système en production. Le directeur a besoin d'une vue consolidée, stable et lisible — pas d'un accès brut aux tables.

## Partie D — Introduction à la BI

**13. Qu'est-ce que la Business Intelligence ?**
La BI est l'ensemble des méthodes, outils et processus qui permettent de collecter, consolider, analyser et restituer les données d'une organisation pour aider à la prise de décision.

**14. Quels sont ses objectifs ?**
Fournir une vue unifiée et fiable des données, faciliter la prise de décision, détecter des tendances, mesurer la performance via des KPI, et anticiper plutôt que subir.

**15. Quelle différence entre une base opérationnelle et un système décisionnel ?**
La base opérationnelle (OLTP) gère les transactions du quotidien, en écriture, avec des données détaillées et changeantes. Le système décisionnel (OLAP / Data Warehouse) gère l'analyse, en lecture, avec des données historisées et agrégées, optimisées pour interroger de gros volumes rapidement.

**16. Pourquoi la BI est-elle indispensable aujourd'hui ?**
Les organisations génèrent un volume croissant de données réparties sur des systèmes hétérogènes. Sans BI, ces données restent des silos inexploités ; avec elle, elles deviennent un avantage stratégique pour piloter l'activité et prendre des décisions basées sur des faits plutôt que sur l'intuition.

## Cas pratique — EduSmart

Le Directeur Général souhaite connaître : le nombre réel d'étudiants, le chiffre d'affaires, le taux de réussite, la satisfaction des étudiants, les formations les plus suivies, le temps moyen de connexion, les enseignants les mieux évalués.

**Où se trouvent ces données ?**
Réparties dans les 5 sources : PostgreSQL (étudiants, paiements), MySQL (notes, connexions), CSV (enseignants), JSON/MongoDB (logs mobile), Redis (temps réel).

**Une seule source suffit-elle ?**
Non, aucune des questions du DG ne peut être répondue avec une seule source.

**Peut-on construire directement un tableau de bord sur les cinq sources ?**
Non — les identifiants diffèrent, les formats sont hétérogènes (SQL, JSON, clé-valeur), et interroger 5 systèmes en direct à chaque clic serait lent et fragile.

**Quels problèmes rencontrera-t-on ?**
Incohérence des identifiants, doublons, latence, absence d'historique, difficulté à croiser des types de données différents.

**Quelle solution proposeriez-vous ?**
Construire un pipeline ETL/ELT qui extrait, nettoie et unifie les 5 sources dans un Data Warehouse, avec un modèle multidimensionnel adapté aux besoins de reporting, puis brancher Power BI dessus.