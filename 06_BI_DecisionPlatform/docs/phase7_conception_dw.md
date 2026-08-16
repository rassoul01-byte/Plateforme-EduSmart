# Phase 7 — Conception du Data Warehouse

## Objectif
Passer d'une collection de tables sources à un modèle pensé pour l'analyse : dimensions, faits, mesures, hiérarchies, granularité.

## Recherche

**Dimensions**
Une dimension décrit le contexte d'un événement métier : qui, quoi, où, quand. Elle contient des attributs descriptifs (nom, catégorie, ville) utilisés pour filtrer et regrouper les analyses, mais pas de valeurs numériques à additionner.

**Faits**
Une table de faits enregistre les événements mesurables de l'activité (un paiement, une note, une connexion). Chaque ligne représente un événement précis, relié aux dimensions par des clés étrangères, et contient les mesures associées.

**Mesures**
Une mesure est une valeur numérique contenue dans une table de faits, sur laquelle on applique des agrégations (somme, moyenne, comptage) : un montant, une note, une durée.

**Hiérarchies**
Une hiérarchie organise les attributs d'une dimension par niveaux emboîtés, permettant de naviguer du général au détail (ex. Dimension Temps : Année -> Trimestre -> Mois -> Jour ; Dimension Région : Pays -> Région -> Ville).

**Granularité**
La granularité définit le niveau de détail d'une table de faits : une ligne par paiement individuel (granularité fine) vs une ligne par total mensuel (granularité grossière). Plus la granularité est fine, plus on peut analyser en détail, mais plus le volume de données est important.

## TP — Identification pour EduSmart

### Dimensions identifiées

| Dimension | Attributs clés | Source(s) |
|---|---|---|
| Dim_Temps | date, jour, mois, trimestre, année, jour_semaine | généré (calendrier) |
| Dim_Etudiant | matricule, nom, prénom, sexe, ville, date_naissance | postgres_etudiants |
| Dim_Formation | filière, classe, cours, module | postgres_classes/filieres, mysql_cours/modules |
| Dim_Enseignant | nom, prénom, diplôme, type_contrat, département | csv_enseignants |
| Dim_Region | ville, département/région | postgres_etudiants.ville, csv_departements |

### Faits identifiés

| Table de faits | Granularité | Dimensions liées | Source |
|---|---|---|---|
| Fait_Paiements | 1 ligne par paiement | Temps, Étudiant | postgres_paiements |
| Fait_Notes | 1 ligne par note obtenue à un quiz/cours | Temps, Étudiant, Formation | mysql_notes |
| Fait_Connexions | 1 ligne par session de connexion | Temps, Étudiant | mysql_temps_connexion, redis_sessions |
| Fait_Quiz | 1 ligne par quiz passé | Temps, Étudiant, Formation | mysql_quiz, redis_last_quiz |

### Mesures identifiées

| Mesure | Table de faits | Type d'agrégation typique |
|---|---|---|
| montant | Fait_Paiements | somme (chiffre d'affaires) |
| note | Fait_Notes | moyenne (taux de réussite, moyenne par formation) |
| duree | Fait_Connexions | moyenne (temps moyen de connexion) |
| nombre_connexions | Fait_Connexions | comptage (étudiants actifs) |

## Conclusion

Cette identification des dimensions, faits et mesures prépare directement la modélisation multidimensionnelle (Phase 8), où le choix entre schéma en étoile et schéma en flocon déterminera la structure physique de ces tables dans le Data Warehouse.