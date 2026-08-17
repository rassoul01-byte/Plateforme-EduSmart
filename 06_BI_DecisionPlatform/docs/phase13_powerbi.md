# Phase 13 — Power BI

## Objectif
Construire un tableau de bord interactif à partir du Data Warehouse EduSmart : modèle relationnel, mesures, KPI, visualisations.

## Environnement utilisé

Power BI Desktop étant réservé à Windows, le tableau de bord a été construit via **Power BI Service** (app.powerbi.com), accessible depuis un navigateur sur Linux/Mac. Les données du Data Warehouse (`edusmart_dw`) ont été exportées en CSV via `\copy`, puis fusionnées en un classeur Excel multi-onglets (`EduSmart_DW.xlsx`) via un script Python, avant import dans Power BI Service.

## Modèle relationnel

Le modèle Power BI reprend le star schema construit en Phase 8 : les tables de faits (`fait_paiements`, `fait_notes`) sont reliées aux dimensions (`dim_temps`, `dim_etudiant`, `dim_formation`, `dim_region`, `dim_enseignant`) par des relations un-à-plusieurs sur les clés correspondantes (`temps_id`, `etudiant_key`, `formation_key`).

**Limite identifiée** : `dim_enseignant` n'a pas de relation directe avec les tables de faits existantes, car aucune table de faits ne référence d'`enseignant_key`. Un visuel tentant de croiser enseignants et notes échoue avec une erreur `ExecuteSemanticQueryUnknownError`, confirmant qu'aucun chemin de relation n'existe dans le modèle. Amélioration future : ajouter une clé `enseignant_key` à `dim_formation` ou à une future table de faits liant enseignants et cours.

## Mesures DAX créées

Taux de réussite (pourcentage de notes >= seuil de passage) :

```dax
Taux Reussite = 
VAR SeuilPassage = 10
RETURN
DIVIDE(
    COUNTROWS(FILTER(fait_notes, fait_notes[note] >= SeuilPassage)),
    COUNTROWS(fait_notes),
    0
) * 100
```

## Tableau de bord construit

Quatre visuels fonctionnels, chacun cohérent avec les choix de visualisation définis en Phase 12 :

| Visuel | Type | KPI représenté |
|---|---|---|
| Carte | Chiffre d'affaires total (5,23 Md) | Chiffre d'affaires |
| Courbe | Chiffre d'affaires par année | Tendance temporelle du chiffre d'affaires |
| Carte | Taux de réussite (50,83 %) | Taux de réussite |
| Barplot | Chiffre d'affaires par ville | Comparaison régionale du chiffre d'affaires |

## Observations

Le pic de chiffre d'affaires visible en 2025, suivi d'une baisse en 2026, confirme la valeur du modèle multidimensionnel : cette information n'aurait pas été visible depuis les tables opérationnelles brutes, mais devient immédiate une fois les données consolidées dans le Data Warehouse et reliées via le star schema.