# Phase 16 — Projet individuel

## Objectif
Consolider l'ensemble du travail réalisé en un projet individuel cohérent, couvrant toute la chaîne décisionnelle : de la donnée opérationnelle au tableau de bord.

## Synthèse du travail réalisé

### Pipeline ETL développé et intégré
Le pipeline complet (`06_BI_DecisionPlatform/etl/`) extrait les 5 sources EduSmart (PostgreSQL, MySQL, CSV, JSON/logs mobile, Redis), les nettoie et les charge dans un Data Warehouse PostgreSQL (`edusmart_dw`), avec traçabilité complète (métadonnées, journal d'exécution) et contrôle qualité automatisé.

### Participation à la construction du Data Warehouse
Un schéma multidimensionnel en étoile (Fact Constellation) a été conçu et implémenté : 5 dimensions (Temps, Étudiant, Formation, Enseignant, Région) et 4 tables de faits (Paiements, Notes, Connexions, Quiz), avec gestion de l'historique via SCD Type 2 sur `dim_etudiant`.

### Schéma multidimensionnel proposé
Le choix du Star Schema (plutôt que Snowflake) a été justifié par la priorité donnée à la simplicité et à la rapidité des requêtes pour des KPI de direction, cohérent avec l'architecture Data Warehouse retenue en Phase 3.

### KPI définis
8 KPI ont été identifiés et rattachés à des tables de faits précises : chiffre d'affaires, taux de réussite, taux d'abandon, progression moyenne, satisfaction, nombre d'étudiants actifs, temps moyen de connexion, enseignants les mieux évalués — répondant directement aux besoins exprimés par le Directeur Général en Phase 1.

### Tableau de bord construit
Un rapport Power BI Service a été construit à partir du Data Warehouse, avec un modèle relationnel reproduisant le star schema, une mesure DAX personnalisée (taux de réussite), et 4 visuels fonctionnels (carte KPI, courbe temporelle, barplot régional).

### Rapport d'analyse
Le pic de chiffre d'affaires en 2025 suivi d'une baisse en 2026, ainsi qu'un taux de réussite global de 50,83%, constituent les deux insights principaux identifiés (Phase 14), avec une recommandation d'investigation ciblée sur ces deux signaux.

## Validation

L'ensemble du pipeline a été testé via une suite de 5 tests automatisés (Phase 15), tous réussis, garantissant la fiabilité des données consolidées avant toute prise de décision basée dessus.