# Phase 9 — Gestion de l'historique (Slowly Changing Dimensions)

## Objectif
Comprendre comment gérer les changements de valeurs dans une dimension au fil du temps, sans perdre l'information historique.

## Recherche

**Pourquoi conserver l'historique des dimensions ?**
Parce que les attributs d'une dimension changent avec le temps (un étudiant déménage, un enseignant change de type de contrat). Si on écrase simplement l'ancienne valeur, on perd la capacité d'analyser correctement le passé : un rapport sur les paiements passés attribuerait à tort la ville actuelle de l'étudiant à des événements qui se sont produits quand il vivait ailleurs.

**SCD Type 1 — Écrasement**
La nouvelle valeur remplace simplement l'ancienne, sans garder de trace du changement. Simple à mettre en œuvre, mais on perd totalement l'historique. Adapté quand l'ancienne valeur n'a aucune importance analytique.

**SCD Type 2 — Nouvelle ligne**
Chaque changement crée une nouvelle ligne dans la dimension, avec des dates de validité (date_debut, date_fin) et un indicateur de ligne active (est_actuel). L'historique complet est conservé, et chaque fait reste lié à la version de la dimension qui était valide au moment de l'événement.

**SCD Type 3 — Ancienne valeur en colonne**
On ajoute une colonne supplémentaire pour stocker uniquement la valeur précédente. Simple, mais ne conserve qu'un seul changement dans le passé.

## Cas pratique — Un étudiant change de ville

**Que faut-il conserver ?**
Il faut conserver à la fois l'ancienne ville et la nouvelle, avec les dates pendant lesquelles chacune était valide, pour que tout fait passé reste rattaché à la ville réelle de l'étudiant au moment de l'événement.

**Pourquoi ?**
Parce qu'un tableau de bord régional (chiffre d'affaires par ville) serait faussé si tous les paiements passés d'un étudiant étaient réattribués à sa nouvelle ville après un déménagement.

## Choix retenu pour EduSmart : SCD Type 2 sur dim_etudiant

Cohérent avec l'usage attendu (Phase 1) : le DG veut suivre l'évolution des KPI par région dans le temps, donc l'attribut ville doit être historisé.

## TP — Implémentation

La table `dim_etudiant` a été étendue avec trois colonnes : `date_debut`, `date_fin`, `est_actuel`. Le script `06_BI_DecisionPlatform/etl/scd_manager.py` compare, à chaque exécution, les valeurs actuelles de la source (`stg_postgres_etudiants`) à la version active de chaque étudiant dans `dim_etudiant` :

- si l'étudiant est nouveau, il est inséré avec `est_actuel = TRUE`
- si un attribut suivi (actuellement `ville`) a changé, l'ancienne ligne est clôturée (`est_actuel = FALSE`, `date_fin` = aujourd'hui) et une nouvelle ligne est créée avec la nouvelle valeur
- si rien n'a changé, la ligne reste inchangée

### Test de validation

Un changement de ville a été simulé sur un étudiant (`Dakar -> Thiès`), suivi d'un cycle complet extract -> transform -> load -> apply_scd2. Résultat :

| etudiant_id | ville | date_debut | date_fin | est_actuel |
|---|---|---|---|---|
| 4 | Dakar | 2026-08-16 | 2026-08-17 | false |
| 4 | Thiès | 2026-08-17 | (null) | true |

Les deux versions coexistent dans la table, confirmant que l'implémentation SCD Type 2 conserve bien l'historique complet sans perte d'information, tout en exposant clairement la version actuellement valide via `est_actuel`.