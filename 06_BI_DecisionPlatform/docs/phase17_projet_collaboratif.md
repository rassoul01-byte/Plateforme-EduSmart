# Phase 17 — Projet collaboratif

## Objectif
Chaque membre du groupe apporte sa source de données ; ensemble, le groupe produit un pipeline ETL unique, un Data Warehouse commun, une base multidimensionnelle, un cube OLAP, un tableau de bord Power BI, et un rapport décisionnel complet.

## Position du projet EduSmart dans cette phase

Le projet réalisé individuellement (Phases 1 à 16) couvre déjà les 5 sources de données du groupe EduSmart (PostgreSQL, MySQL, CSV, logs mobile, Redis), simulant en solo l'intégration que la Phase 17 demande normalement en groupe. Ce travail peut donc servir de base directe à la version collaborative, avec les ajustements suivants à anticiper :

### Points de coordination avec le groupe
- **Cohérence des identifiants** : si d'autres membres du groupe ont généré leurs propres jeux de données pour les mêmes sources, il faudra s'assurer que les `etudiant_id` (ou équivalents) restent cohérents entre toutes les sources fusionnées, pour éviter les orphelins détectés en Phase 15.
- **Fusion des pipelines ETL** : chaque script `extract_*.py` développé individuellement peut être repris tel quel dans le pipeline commun, à condition d'harmoniser la configuration (`config.py`) sur des paramètres de connexion partagés par le groupe.
- **Data Warehouse unique** : le schéma `edusmart_dw` construit en Phase 8 peut servir de structure cible commune, à condition que tous les membres s'accordent sur les mêmes définitions de dimensions et de faits avant l'intégration finale.
- **Cube OLAP et tableau de bord partagés** : les opérations OLAP (Phase 10) et le dashboard Power BI (Phase 13) construits individuellement montrent la faisabilité technique ; en groupe, ils seraient enrichis avec les KPI et visualisations complémentaires apportés par les autres membres (ex. enseignants les mieux évalués une fois `dim_enseignant` correctement relié).

## Rapport décisionnel complet

Le rapport final combine les éléments déjà produits : contexte métier (Phase 1-2), choix d'architecture (Phase 3-4), qualité et métadonnées (Phase 5-6), modélisation (Phase 7-9), analyse OLAP et KPI (Phase 10-11), visualisation et tableau de bord (Phase 12-13), storytelling (Phase 14), et validation (Phase 15) — formant une chaîne complète et documentée, prête à être présentée (Phase 18).