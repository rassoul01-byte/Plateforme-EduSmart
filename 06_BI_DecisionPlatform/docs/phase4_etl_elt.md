# Phase 4 — ETL ou ELT ?

## Objectif
Comprendre la différence entre ETL et ELT, et choisir l'approche adaptée à EduSmart.

## Recherche

**1. Qu'est-ce qu'un ETL ?**
ETL (Extract, Transform, Load) est une approche où les données sont extraites des sources, transformées et nettoyées avant d'être chargées dans la cible finale (le Data Warehouse). La donnée qui arrive dans le DW est donc déjà propre et prête à l'usage.

**2. Qu'est-ce qu'un ELT ?**
ELT (Extract, Load, Transform) inverse l'ordre : les données brutes sont chargées telles quelles dans la cible (souvent un Data Lake ou un entrepôt cloud très puissant), puis transformées à la demande, directement dans le système cible.

**3. Quelles différences ?**

| Critère | ETL | ELT |
|---|---|---|
| Où se fait la transformation | Avant chargement, sur un serveur intermédiaire | Après chargement, dans la cible |
| Puissance requise | Serveur ETL dédié | Cible très puissante (cloud DW) |
| Données stockées | Uniquement les données transformées | Brutes + transformées |
| Flexibilité | Moins flexible (schéma fixé avant) | Plus flexible (re-transformer à volonté) |
| Cas d'usage typique | Data Warehouse classique | Data Lake / Cloud (Snowflake, BigQuery) |

**4. Dans quels cas choisir l'un ou l'autre ?**
L'ETL est préférable quand la cible est un Data Warehouse relationnel classique avec des ressources de calcul limitées, et quand on veut garantir la qualité avant stockage. L'ELT est préférable avec un entrepôt cloud très puissant (Snowflake, BigQuery, Databricks) ou un Data Lake, où l'on préfère garder toute la donnée brute disponible pour des transformations multiples et évolutives.

## Choix retenu pour EduSmart : ETL

Cohérent avec le choix d'architecture Data Warehouse fait en Phase 3 : les données sont nettoyées et validées avant d'entrer dans l'entrepôt, ce qui garantit des KPI fiables dès la première requête, sans dépendre d'un moteur cloud puissant pour transformer à la volée.

## TP — Pipeline développé

Le pipeline ETL a été développé dans `06_BI_DecisionPlatform/etl/` avec la structure suivante :

- `config.py` : configuration centralisée des connexions aux 5 sources et à la base cible du Data Warehouse
- `extract_postgres.py` : extraction de la Source 1 (PostgreSQL — Académique)
- `extract_mysql.py` : extraction de la Source 2 (MySQL — Learning)
- `extract_csv.py` : extraction de la Source 3 (CSV — Ressources Humaines)
- `extract_mongodb.py` : extraction de la Source 4 (Logs mobile, JSON/JSONL ou MongoDB)
- `extract_redis.py` : extraction de la Source 5 (Redis — Temps réel)
- `transform.py` : nettoyage des données extraites (suppression des doublons, gestion des valeurs manquantes, uniformisation des colonnes)
- `load.py` : chargement des données propres dans le Data Warehouse PostgreSQL (`edusmart_dw`)
- `run_pipeline.py` : orchestrateur exécutant l'ensemble du pipeline Extract → Transform → Load

### Résultat de l'exécution

Le pipeline complet s'exécute en environ 21 secondes et charge 20 tables de staging dans le Data Warehouse, couvrant l'intégralité des 5 sources :

- PostgreSQL : étudiants (15 150), inscriptions (18 000), paiements (30 000), classes (220), filières (15)
- MySQL : notes (45 350), progression (55 000), temps de connexion (70 000), cours (120), quiz (150), modules (20)
- CSV : enseignants (450), départements (8), salaires (3500), absences (1400)
- Logs mobile : 112 280 événements chargés
- Redis : sessions (3517), progression temps réel (7481), derniers quiz (3500), notifications (7041)

### Point d'attention identifié : fraîcheur des données (freshness)

Certaines clés Redis (sessions, progression temps réel) sont créées avec une durée de vie limitée (TTL) pour simuler des données réellement temps réel. Si le pipeline ETL est exécuté trop longtemps après l'insertion des données, ces clés ont expiré et l'extraction renvoie 0 ligne. Cela illustre un enjeu réel de la BI : les sources temps réel doivent être extraites à intervalles rapprochés (extraction programmée) plutôt que de façon ponctuelle, sous peine de perdre des données avant même qu'elles n'atteignent le Data Warehouse.