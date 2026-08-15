# Phase 3 — Les architectures décisionnelles

## Objectif
Étudier les grandes architectures de stockage et de traitement des données décisionnelles.

## Data Warehouse

**Définition** : Entrepôt de données centralisé, structuré, qui stocke des données historisées, nettoyées et transformées, organisées autour de sujets métier (ventes, étudiants, formations) plutôt qu'autour des applications qui les produisent.

**Architecture** : Sources opérationnelles -> ETL (extraction, transformation, chargement) -> modèle relationnel/multidimensionnel (schéma en étoile ou flocon) -> outils de reporting (Power BI, Tableau).

**Avantages** : Données fiables et cohérentes, performances élevées pour les requêtes analytiques, historique conservé, structure stable adaptée aux KPI.

**Limites** : Coût et temps de mise en place (schéma défini à l'avance), peu flexible pour des données non structurées, les transformations en amont peuvent faire perdre le détail brut.

**Cas d'utilisation** : Reporting financier, tableaux de bord de direction, analyses récurrentes avec des indicateurs stables (chiffre d'affaires, taux de réussite).

## Data Mart

**Définition** : Sous-ensemble d'un Data Warehouse, focalisé sur un seul domaine métier ou un seul service (ex. un Data Mart "RH" ou un Data Mart "Pédagogie").

**Architecture** : Peut être alimenté directement depuis les sources, ou extrait à partir du Data Warehouse central (approche descendante, recommandée).

**Avantages** : Rapide à mettre en place, ciblé sur les besoins d'un service précis, performances optimisées pour un périmètre restreint.

**Limites** : Risque de silos si chaque service crée son propre Data Mart sans cohérence globale, duplication de données, incohérences entre Data Marts si non alignés sur un modèle commun.

**Cas d'utilisation** : Un Data Mart dédié à la direction pédagogique d'EduSmart pour suivre uniquement les notes, quiz et progression, sans les données RH ou financières.

## Data Lake

**Définition** : Stockage centralisé qui conserve les données dans leur format brut (structuré, semi-structuré, non structuré) sans transformation préalable, à grande échelle et à faible coût.

**Architecture** : Sources variées -> ingestion brute (souvent via un système de fichiers distribué ou du stockage objet type S3) -> transformation à la demande au moment de l'analyse (schema-on-read).

**Avantages** : Très flexible, accepte tous types de données (logs JSON, vidéos, CSV), coût de stockage faible, adapté au Big Data et au Machine Learning.

**Limites** : Risque de devenir un "data swamp" (marécage de données) sans gouvernance, pas optimisé nativement pour les requêtes analytiques rapides, qualité des données non garantie à l'entrée.

**Cas d'utilisation** : Stocker les logs bruts de l'application mobile EduSmart (JSON) avant tout traitement, en gardant toute la richesse d'origine pour de futures analyses ou du machine learning.

## Data Lakehouse

**Définition** : Architecture hybride qui combine la flexibilité de stockage du Data Lake avec les capacités de gestion, de performance et de fiabilité transactionnelle du Data Warehouse.

**Architecture** : Stockage unique (souvent sur du stockage objet) avec une couche de gestion (type Delta Lake, Apache Iceberg) qui apporte transactions ACID, versionning de schéma, et permet à la fois requêtes SQL analytiques et traitements Big Data/ML sur les mêmes données.

**Avantages** : Une seule copie des données pour tous les usages (BI et data science), coût réduit par rapport à maintenir Data Lake + Data Warehouse séparés, gouvernance et qualité renforcées.

**Limites** : Écosystème encore jeune et en évolution rapide, complexité de mise en œuvre, nécessite des compétences pointues, moins mature que le Data Warehouse classique pour du reporting pur.

**Cas d'utilisation** : Une plateforme qui veut à la fois faire du reporting Power BI classique ET entraîner des modèles de machine learning (ex. prédire le décrochage scolaire) sur les mêmes données EduSmart.

## Tableau comparatif

| Critère | Data Warehouse | Data Mart | Data Lake | Data Lakehouse |
|---|---|---|---|---|
| Type de données | Structurées | Structurées | Tous types | Tous types |
| Transformation | Avant stockage (ETL) | Avant stockage | Après extraction (ELT) | Flexible |
| Coût | Élevé | Modéré | Faible | Modéré |
| Performance analytique | Très bonne | Très bonne (périmètre réduit) | Variable | Bonne |
| Gouvernance | Forte | Forte (si bien géré) | Faible si mal géré | Forte |
| Usage principal | Reporting BI | Reporting ciblé par service | Big Data / ML | BI + ML unifiés |

## Cas pratique — Quelle architecture pour EduSmart ?

**Choix proposé : Data Warehouse**, avec une réflexion vers un Data Lakehouse comme évolution future.

**Justification** :

- Le besoin principal exprimé (Phase 1) est du reporting décisionnel classique : chiffre d'affaires, taux de réussite, KPI de direction — exactement le cas d'usage central du Data Warehouse.
- Les 5 sources d'EduSmart sont majoritairement structurées ou semi-structurées (PostgreSQL, MySQL, CSV, JSON, Redis), donc adaptées à un modèle multidimensionnel classique (schéma en étoile) sans complexité inutile.
- Le volume de données reste modéré (dizaines de milliers de lignes, pas des téraoctets) — un Data Lake ou Lakehouse serait surdimensionné à ce stade.
- Un Data Warehouse apporte la fiabilité, la cohérence et les performances nécessaires pour des KPI stables consultés quotidiennement par la direction.
- Si le projet évolue plus tard vers du machine learning (ex. prédiction de décrochage à partir des logs bruts), une architecture Lakehouse deviendrait pertinente pour combiner reporting et exploitation des données brutes JSON sans les dénaturer.