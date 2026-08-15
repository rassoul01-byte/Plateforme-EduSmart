# Phase 5 — Contrôle qualité des données

## Objectif
Comprendre qu'un ETL ne consiste pas seulement à déplacer des données, mais aussi à garantir leur qualité.

## Recherche

**Qu'est-ce que la qualité des données ?**
La qualité des données mesure à quel point les données sont fiables, exploitables et conformes à la réalité qu'elles sont censées représenter. Une donnée de mauvaise qualité fausse les KPI et peut conduire à de mauvaises décisions, même si le pipeline technique fonctionne parfaitement.

### Les 5 dimensions étudiées

- **Complétude** : toutes les informations nécessaires sont-elles présentes ? (ex. un étudiant sans email, un paiement sans montant)
- **Unicité** : chaque enregistrement existe-t-il une seule fois ? (ex. un même enseignant dupliqué à cause d'une synchronisation ratée entre sources)
- **Cohérence** : les données respectent-elles des règles logiques et sont-elles alignées entre elles ? (ex. une date de paiement antérieure à la date d'inscription)
- **Exactitude** : les données reflètent-elles fidèlement la réalité ? (ex. une note supérieure à 20/20, un montant négatif)
- **Fraîcheur** : les données sont-elles à jour au moment de leur utilisation ? (ex. la fraîcheur des données Redis identifiée en Phase 4, où des clés expiraient avant extraction)

## TP — Rapport qualité

Le script `transform.py` a été étendu pour produire un rapport qualité complet à chaque exécution du pipeline, sauvegardé dans `quality_reports/rapport_qualite.csv` et `.md`. Pour chaque table, il enregistre : le nombre de lignes extraites, rejetées, les doublons supprimés, les valeurs manquantes détectées, les incohérences métier détectées, les corrections effectuées, et le nombre de lignes finales.

### Règles de détection d'incohérences appliquées

- `postgres_paiements` : montant négatif
- `mysql_notes` : note en dehors de l'intervalle [0, 20]
- `postgres_etudiants` : email manquant ou vide

### Résultats obtenus (extrait significatif)

| Table | Extraites | Doublons | Manquantes | Incohérences | Corrections | Finales |
|---|---|---|---|---|---|---|
| postgres_etudiants | 15150 | 0 | 5478 | 889 | 5478 | 15150 |
| mongo_logs_mobile | 113435 | 1155 | 154823 | 0 | 154823 | 112280 |
| csv_enseignants | 468 | 18 | 36 | 0 | 36 | 450 |
| redis_notifications | 14082 | 7041 | 0 | 0 | 0 | 7041 |
| mysql_notes | 45350 | 0 | 879 | 0 | 879 | 45350 |

### Analyse détaillée — table `postgres_etudiants`

L'investigation des 5478 valeurs manquantes a révélé leur répartition exacte par colonne :

| Colonne | Valeurs manquantes | Taux |
|---|---|---|
| sexe | 1917 | 12,6 % |
| email | 889 | 5,9 % |
| telephone | 1175 | 7,8 % |
| ville | 1497 | 9,9 % |

Le champ `email` étant identifié comme critique (nécessaire pour contacter l'étudiant), il fait l'objet d'une règle d'incohérence dédiée en plus du simple comptage de valeurs manquantes.

### Corrections automatiques appliquées

Les valeurs manquantes sont automatiquement corrigées lors de la transformation : `"inconnu"` pour les champs textuels, `0` pour les champs numériques, tout en traçant précisément le nombre de corrections effectuées par table. Aucune ligne n'est rejetée dans cette version du pipeline — la stratégie retenue privilégie la correction et la traçabilité plutôt que la suppression, afin de ne pas perdre d'information exploitable (un étudiant sans email reste un étudiant valide pour la plupart des analyses).

### Point notable — logs mobile (Source 4)

La table `mongo_logs_mobile` présente le taux d'anomalies le plus élevé : 154 823 valeurs manquantes et 1155 doublons pour 113 435 événements extraits. Ce résultat est cohérent avec les 21 068 événements à anomalies structurelles générés volontairement lors de la création de cette source (Phase 4), ce qui confirme que le contrôle qualité détecte correctement les défauts injectés dans les données.