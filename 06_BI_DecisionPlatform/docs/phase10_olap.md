# Phase 10 — Analyse multidimensionnelle (OLAP)

## Objectif
Comprendre comment naviguer dans un cube de données pour explorer les KPI sous différents angles.

## Recherche

**Cube OLAP**
Un cube OLAP est une structure de données multidimensionnelle qui organise les mesures (montant, note, durée) selon plusieurs axes d'analyse (dimensions : temps, étudiant, formation, région). Chaque cellule du cube correspond à une mesure agrégée pour une combinaison précise de valeurs de dimensions — par exemple, le chiffre d'affaires pour une ville et un mois donnés.

**Drill Down (forage vers le bas)**
Descendre d'un niveau de détail à un niveau plus fin dans une hiérarchie — ex. passer du chiffre d'affaires annuel au chiffre d'affaires mensuel, puis journalier.

**Roll Up (agrégation vers le haut)**
L'opération inverse : remonter à un niveau plus général — ex. passer du chiffre d'affaires par ville au chiffre d'affaires par région.

**Slice (tranche)**
Fixer la valeur d'une seule dimension pour obtenir une tranche du cube — ex. ne regarder que les données d'une seule ville, toutes autres dimensions confondues.

**Dice (dé, sous-cube)**
Fixer des valeurs sur plusieurs dimensions à la fois pour obtenir un sous-cube plus restreint — ex. ne regarder que les paiements de deux villes précises sur deux années précises.

**Pivot (rotation)**
Réorganiser les axes d'analyse pour changer la perspective sans changer les données — ex. passer d'un tableau "Ville en lignes / Année en colonnes" à l'inverse.

## TP — Explorer le cube EduSmart

Le cube d'analyse repose sur la table de faits `fait_paiements`, reliée aux dimensions `dim_temps` (axe temporel) et `dim_etudiant` (axe géographique via l'attribut `ville`, historisé en SCD Type 2 depuis la Phase 9).

### 1. Vue d'ensemble du cube

Agrégation totale du chiffre d'affaires et du nombre de paiements, tous axes confondus — le point de départ avant toute navigation dans le cube.

### 2. Roll Up — chiffre d'affaires par année

Agrégation du chiffre d'affaires au niveau le plus général de la dimension Temps (l'année), en remontant depuis le détail des paiements individuels.

### 3. Drill Down — détail par mois

Descente d'un niveau dans la hiérarchie temporelle : passage de l'année au mois pour une année donnée, révélant la saisonnalité du chiffre d'affaires.

### 4. Slice — une seule ville

Isolation d'une tranche du cube en fixant la dimension Région à une seule valeur (une ville), pour analyser son chiffre d'affaires indépendamment des autres.

### 5. Dice — sous-cube ville x année

Extraction d'un sous-cube en fixant simultanément deux dimensions (plusieurs villes ET plusieurs années), permettant une comparaison croisée ciblée.

### 6. Pivot — Ville en lignes, Année en colonnes

Réorganisation du même sous-cube sous forme de tableau croisé, avec les villes en lignes et les années en colonnes, facilitant la lecture comparative dans un format proche de ce qu'affichera Power BI (Phase 13).

## Conclusion

Ces six opérations démontrent que le modèle en étoile construit en Phase 8 (table de faits + dimensions) permet de naviguer librement dans les données selon n'importe quel axe et n'importe quel niveau de détail, sans avoir à modifier la structure du Data Warehouse — c'est précisément l'intérêt d'une modélisation multidimensionnelle par rapport à des tables opérationnelles classiques.