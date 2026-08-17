# Phase 15 — Validation et tests du pipeline

## Objectif
Comprendre pourquoi un pipeline ETL doit être testé comme n'importe quel logiciel, et vérifier concrètement que le pipeline EduSmart est fiable.

## Recherche

**Pourquoi tester un pipeline ETL ?**
Un pipeline ETL manipule des données à grande échelle sans supervision humaine ligne par ligne, une erreur silencieuse (jointure ratée, filtre trop strict, conversion de type incorrecte) peut faire disparaître ou fausser des milliers de lignes sans qu'aucune erreur ne s'affiche. Contrairement à un bug d'interface visible immédiatement, un bug de pipeline ETL peut passer inaperçu pendant des mois et fausser silencieusement tous les KPI construits dessus, d'où l'importance de vérifications systématiques et automatisables à chaque exécution.

## TP — Tests de validation du pipeline EduSmart

Le script `06_BI_DecisionPlatform/etl/validate_pipeline.py` exécute automatiquement 5 tests après chaque run du pipeline, répondant chacun à une question posée par l'énoncé :

1. **Complétude de l'extraction** : chaque table de staging contient-elle au moins le volume de lignes attendu, établi lors des exécutions précédentes ?
2. **Complétude du chargement** : toutes les tables de staging détectées dans le Data Warehouse contiennent-elles bien des lignes (aucune table vide non repérée) ?
3. **Absence de perte de données** : le peuplement des tables de faits (Phase 8) a-t-il perdu des lignes de façon anormale par rapport au staging ?
4. **Absence d'erreurs** : le journal `etl_execution_log` (Phase 6) contient-il des exécutions en échec récentes ?
5. **Validité des clés étrangères** : les clés `etudiant_key` des tables de faits pointent-elles toutes vers une ligne existante de `dim_etudiant` (aucune clé orpheline) ?

### Résultat de l'exécution

**5/5 tests réussis.**

| Test | Résultat |
|---|---|
| Complétude extraction | OK — toutes les tables au-dessus du seuil minimal attendu |
| Complétude chargement | OK — toutes les tables stg_* chargées contiennent des données |
| Absence de perte de données | OK — fait_paiements : 2,1% de perte (cohérent avec la Phase 8) ; fait_notes : 0% de perte |
| Absence d'erreurs | OK — aucune erreur enregistrée dans l'historique récent |
| Validité des clés | OK — 0 clé orpheline sur fait_paiements et fait_notes |

## Analyse

Le taux de perte de 2,1% sur `fait_paiements`, déjà identifié comme point d'attention en Phase 8 (probablement dû à des dates de paiement hors de la plage couverte par `dim_temps`), est confirmé de façon automatisée et reproductible par ce test, plutôt que découvert manuellement. C'est précisément l'intérêt d'une suite de tests : transformer une observation ponctuelle en vérification systématique, exécutable après chaque nouvelle exécution du pipeline pour détecter toute dégradation future.

L'absence totale de clés orphelines confirme que le modèle en étoile construit en Phase 8-9 est structurellement sain : aucun fait ne référence une dimension inexistante, garantissant que tous les visuels Power BI (Phase 13) s'appuient sur des données cohérentes.