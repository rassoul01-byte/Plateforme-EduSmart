# Phase 8 — Modélisation multidimensionnelle

## Objectif
Choisir la structure physique du Data Warehouse à partir des dimensions et faits identifiés en Phase 7.

## Recherche

**Star Schema (schéma en étoile)**
Une table de faits centrale, reliée directement à des tables de dimensions dénormalisées (chaque dimension est une seule table plate, sans sous-niveaux séparés).

**Snowflake Schema (schéma en flocon)**
Variante du schéma en étoile où les dimensions sont normalisées, éclatées en plusieurs tables liées entre elles (ex. Dim_Ville -> Dim_Region -> Dim_Pays au lieu d'une seule table Dim_Region avec tous les attributs).

**Fact Constellation (constellation de faits)**
Plusieurs tables de faits partagent certaines dimensions communes (ex. Fait_Paiements et Fait_Notes partagent tous deux Dim_Etudiant et Dim_Temps) — c'est en réalité plusieurs schémas en étoile imbriqués.

### Comparaison

| Critère | Star Schema | Snowflake Schema |
|---|---|---|
| Structure des dimensions | Dénormalisées (une table plate) | Normalisées (plusieurs tables liées) |
| Nombre de jointures | Peu (rapide) | Plus nombreuses (plus lent) |
| Redondance des données | Plus élevée | Réduite |
| Simplicité pour l'utilisateur métier | Très simple à comprendre | Plus complexe |
| Performance requêtes | Meilleure | Moins bonne (plus de jointures) |
| Espace de stockage | Plus important | Optimisé |

## TP — Modèle retenu pour EduSmart

**Choix : Star Schema, en architecture Fact Constellation** puisque plusieurs tables de faits (Paiements, Notes) partagent des dimensions communes (Etudiant, Temps).

**Justification** : cohérent avec le choix Data Warehouse classique de la Phase 3 — on privilégie la simplicité et la rapidité des requêtes pour des KPI de direction, plutôt que l'optimisation du stockage. Le volume de données reste modéré, donc la redondance du star schema n'est pas un problème.

### Schéma physique créé

5 dimensions et 4 tables de faits ont été créées dans `edusmart_dw` via `06_BI_DecisionPlatform/data_warehouse/create_dw_schema.sql` :

- **Dimensions** : dim_temps, dim_etudiant, dim_formation, dim_enseignant, dim_region
- **Faits** : fait_paiements, fait_notes, fait_connexions, fait_quiz

Chaque table de faits référence ses dimensions par clé étrangère, avec des index créés sur ces clés pour optimiser les jointures.

### Peuplement du schéma

Le script `06_BI_DecisionPlatform/etl/populate_dw.py` peuple les dimensions et faits à partir des tables de staging (`stg_*`) déjà chargées par le pipeline ETL.

**Résultat de l'exécution :**

| Table | Lignes |
|---|---|
| dim_temps | 1826 (calendrier 2022-2026) |
| dim_etudiant | 15150 |
| dim_formation | 220 |
| dim_enseignant | 450 |
| dim_region | 10 |
| fait_paiements | 29383 / 30000 sources |
| fait_notes | 45350 / 45350 sources (100%) |

### Point d'attention

617 paiements (2%) n'ont pas été intégrés dans `fait_paiements`, probablement dus à des dates de paiement en dehors de la plage couverte par `dim_temps` (2022-2026) ou à un format de date non standard. Ce constat illustre concrètement l'importance du contrôle qualité (Phase 5) : une jointure vers une dimension Temps mal calibrée peut faire perdre silencieusement des faits, ce qui justifierait d'élargir la plage de dates ou d'investiguer les dates rejetées dans une prochaine itération.