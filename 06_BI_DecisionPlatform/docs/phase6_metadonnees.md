# Phase 6 — Métadonnées et traçabilité

## Objectif
Comprendre pourquoi il ne suffit pas de déplacer des données : il faut aussi savoir d'où elles viennent, quand elles ont été extraites, et dans quel état.

## Recherche

**Pourquoi conserver la source ?**
Pour savoir précisément d'où provient chaque donnée chargée dans le Data Warehouse (PostgreSQL, MySQL, CSV, JSON, Redis). En cas d'anomalie détectée dans un KPI, on doit pouvoir remonter immédiatement au système d'origine sans deviner.

**Pourquoi conserver la date d'extraction ?**
Pour connaître la fraîcheur d'une donnée au moment où elle a été intégrée — essentiel pour des sources comme Redis où les données peuvent expirer ou changer rapidement, et pour distinguer des exécutions différentes du pipeline.

**Pourquoi conserver la version ?**
Pour suivre l'évolution du pipeline lui-même (changement de schéma, de règles de transformation) et pouvoir expliquer pourquoi deux exécutions du même pipeline donnent des résultats différents.

**Pourquoi conserver le nombre de lignes ?**
Pour détecter automatiquement une anomalie de volume : une extraction qui ramène soudain beaucoup moins de lignes signale probablement un problème de connexion ou une source vide, sans avoir à comparer manuellement à chaque fois.

**Pourquoi conserver le statut du traitement ?**
Pour savoir immédiatement si une exécution s'est terminée avec succès, a échoué, ou a réussi partiellement — indispensable pour automatiser des alertes et faire confiance (ou non) aux données actuellement dans le Data Warehouse.

## TP — Tables de métadonnées

Deux tables ont été créées dans le Data Warehouse via `06_BI_DecisionPlatform/etl/metadata_tracker.py` :

### `metadata_sources`
Reflète l'état courant de chaque source (une ligne par source, mise à jour à chaque exécution) :

| Colonne | Description |
|---|---|
| source | nom de la source (postgres, mysql, csv_rh, logs_mobile, redis) |
| derniere_extraction | horodatage de la dernière extraction réussie |
| version | version du pipeline ETL |
| nombre_lignes | nombre de lignes extraites lors de la dernière exécution |
| statut | succes / echec |

### `etl_execution_log`
Historique complet de toutes les exécutions du pipeline, jamais écrasé :

| Colonne | Description |
|---|---|
| id | identifiant auto-incrémenté de l'exécution |
| source | source concernée |
| date_execution | horodatage de l'exécution |
| duree_secondes | durée de l'extraction |
| nombre_lignes | nombre de lignes extraites |
| erreurs | message d'erreur éventuel |
| statut | succes / echec |

## Résultat de l'exécution

Exemple de contenu de `metadata_sources` après une exécution du pipeline :

| source | dernière extraction | version | lignes | statut |
|---|---|---|---|---|
| postgres | 2026-08-16 21:27:56 | 1.0 | 63385 | succes |
| mysql | 2026-08-16 21:27:57 | 1.0 | 170640 | succes |
| csv_rh | 2026-08-16 21:27:57 | 1.0 | 5376 | succes |
| logs_mobile | 2026-08-16 21:27:58 | 1.0 | 113435 | succes |
| redis | 2026-08-16 21:28:00 | 1.0 | 36786 | succes |

Le journal `etl_execution_log` confirme les durées d'extraction par source (de 0.03s pour le CSV RH à 2.09s pour Redis), permettant de repérer facilement les sources les plus lentes du pipeline.

## Bénéfice concret

Ces deux tables transforment le pipeline ETL en système traçable et auditable : en cas de chiffre suspect dans un futur dashboard Power BI, il devient possible de vérifier en quelques secondes si la donnée provient d'une extraction récente et réussie, ou si une source a échoué silencieusement.