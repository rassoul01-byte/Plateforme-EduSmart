# Phase 18 — Présentation

## Plan de présentation (11 points)

### 1. Le contexte métier
EduSmart est une plateforme de formation en ligne dont les données sont réparties sur 5 systèmes hétérogènes. Le Directeur Général a besoin d'une vue consolidée pour piloter l'activité (Phase 1-2).

### 2. Les sources de données
PostgreSQL (académique), MySQL (pédagogique), CSV (RH), JSON/logs mobile, Redis (temps réel) — 5 sources aux formats et identifiants différents.

### 3. Les difficultés d'intégration
Identifiants hétérogènes entre sources, formats variés (SQL, JSON, clé-valeur), et données temps réel avec TTL pouvant expirer avant extraction (Phase 4).

### 4. Le pipeline ETL/ELT
Choix d'un pipeline ETL (Phase 4) : extraction, transformation et nettoyage avant chargement, cohérent avec l'architecture Data Warehouse classique retenue en Phase 3.

### 5. Les contrôles qualité réalisés
Détection de doublons, valeurs manquantes, incohérences métier (montants négatifs, notes hors barème), avec corrections automatiques tracées (Phase 5).

### 6. Les métadonnées produites
Tables `metadata_sources` (état courant) et `etl_execution_log` (historique complet des exécutions), garantissant la traçabilité de chaque donnée chargée (Phase 6).

### 7. Le Data Warehouse
Schéma en étoile (Fact Constellation) avec gestion de l'historique via SCD Type 2 sur les attributs sensibles comme la ville de l'étudiant (Phase 7-9).

### 8. Le modèle multidimensionnel
5 dimensions, 4 tables de faits, avec exploration du cube via les opérations OLAP (drill down, roll up, slice, dice, pivot) démontrées en Phase 10.

### 9. Les KPI retenus
8 KPI définis et justifiés, directement alignés sur les besoins exprimés par le DG en Phase 1 (Phase 11).

### 10. Le tableau de bord Power BI
Modèle relationnel reproduisant le star schema, mesure DAX pour le taux de réussite, 4 visuels fonctionnels révélant un pic de chiffre d'affaires en 2025 (Phase 13).

### 11. Les recommandations stratégiques
Investiguer la baisse de chiffre d'affaires en 2026 avant qu'elle ne s'aggrave, et analyser le taux de réussite par formation pour cibler les cours en difficulté (Phase 14).

## Validation du travail présenté

L'ensemble de la chaîne a été testé et validé automatiquement (Phase 15) : 5/5 tests de qualité et d'intégrité réussis, garantissant que les chiffres présentés reposent sur des données fiables et traçables.