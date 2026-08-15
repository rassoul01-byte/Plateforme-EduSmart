"""
EduSmart - Source 3 : CSV - Ressources Humaines
Génération de 4 fichiers CSV indépendants (comme le ferait un export RH réel),
avec anomalies volontaires : identifiants incompatibles entre fichiers,
doublons, valeurs manquantes, formats de dates hétérogènes, catégories
mal standardisées.

Fichiers produits :
  - departements.csv
  - enseignants.csv
  - salaires.csv
  - absences.csv
"""

import csv
import os
import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker("fr_FR")
random.seed(21)
Faker.seed(21)

OUT_DIR = os.path.dirname(__file__)

N_DEPARTEMENTS = 8
N_ENSEIGNANTS = 450
N_SALAIRES = 3500          # plusieurs lignes de paie par enseignant (historique mensuel)
N_ABSENCES = 1400

DEPARTEMENTS_NOMS = [
    "Informatique", "Gestion & Finance", "Langues", "Sciences Humaines",
    "Génie Civil", "Marketing & Commerce", "Design", "Direction Pédagogique",
]

CONTRATS = ["CDI", "CDD", "Vacataire", "cdi", "Vacataire ", "CDD "]  # espaces/casse -> mal standardisé
DIPLOMES = ["Doctorat", "Master", "Ingenieur", "PhD", "Master 2", "doctorat"]
STATUTS_ABSENCE = ["Maladie", "Conge", "maladie", "conge paye", "Formation",
                    "Absence injustifiee", "CONGE"]

# --------------------------------------------------------------------
# 1. departements.csv
# --------------------------------------------------------------------
departements = []
for i, nom in enumerate(DEPARTEMENTS_NOMS[:N_DEPARTEMENTS], start=1):
    departements.append({
        "departement_id": f"DEP{i:02d}",
        "nom_departement": nom,
        "responsable": fake.name(),
        "budget_annuel": round(random.uniform(5_000_000, 40_000_000), 2),
    })

# --------------------------------------------------------------------
# 2. enseignants.csv
# --------------------------------------------------------------------
enseignants = []
for i in range(1, N_ENSEIGNANTS + 1):
    # Anomalie : formats d'identifiant hétérogènes / incompatibles
    if random.random() < 0.10:
        emp_id = f"{1000 + i}"                # format numérique brut
    elif random.random() < 0.05:
        emp_id = f"ens_{i}"                   # format legacy en minuscules
    else:
        emp_id = f"ENS{i:04d}"                # format standard

    date_embauche = fake.date_between(start_date="-15y", end_date="-30d")
    # Anomalie : ~5% de dates au format texte différent (JJ/MM/AAAA vs AAAA-MM-JJ)
    if random.random() < 0.05:
        date_embauche_str = date_embauche.strftime("%d/%m/%Y")
    else:
        date_embauche_str = date_embauche.strftime("%Y-%m-%d")

    enseignants.append({
        "enseignant_id": emp_id,
        "nom": fake.last_name(),
        "prenom": fake.first_name(),
        # Anomalie : ~7% d'emails manquants
        "email": "" if random.random() < 0.07 else fake.email(),
        "departement_id": random.choice(departements)["departement_id"],
        "diplome": random.choice(DIPLOMES),
        "type_contrat": random.choice(CONTRATS),
        "date_embauche": date_embauche_str,
    })

# Anomalie : quelques doublons stricts (même personne exportée deux fois par le RH)
for _ in range(18):
    dup = random.choice(enseignants).copy()
    enseignants.append(dup)

# --------------------------------------------------------------------
# 3. salaires.csv  (historique mensuel, avec IDs parfois incompatibles)
# --------------------------------------------------------------------
salaires = []
valid_ids = [e["enseignant_id"] for e in enseignants]
for i in range(1, N_SALAIRES + 1):
    ens_id = random.choice(valid_ids)
    # Anomalie : ~4% de lignes référencent un enseignant_id qui n'existe pas
    # dans enseignants.csv (ex: ancien format non repris lors d'une migration)
    if random.random() < 0.04:
        ens_id = f"OLD{random.randint(1,999)}"

    salaire_base = round(random.uniform(250000, 900000), 2)
    prime = round(random.uniform(0, 80000), 2)
    # Anomalie : ~2% de salaires manquants (non renseignés ce mois-ci)
    salaire_base_out = "" if random.random() < 0.02 else salaire_base

    salaires.append({
        "salaire_id": f"SAL{i:05d}",
        "enseignant_id": ens_id,
        "mois": random.choice(["2025-01","2025-02","2025-03","2025-04","2025-05",
                                "2025-06","2025-07","2025-08","2025-09","2025-10",
                                "2025-11","2025-12","2026-01"]),
        "salaire_base": salaire_base_out,
        "prime": prime,
        "devise": "XOF",
    })

# --------------------------------------------------------------------
# 4. absences.csv
# --------------------------------------------------------------------
absences = []
for i in range(1, N_ABSENCES + 1):
    ens_id = random.choice(valid_ids)
    if random.random() < 0.03:
        ens_id = f"UNKNOWN{random.randint(1,50)}"  # orphelin volontaire

    date_debut = fake.date_between(start_date="-2y", end_date="today")
    duree = random.choice([1, 1, 2, 3, 5, 10])
    date_fin = date_debut + timedelta(days=duree)
    # Anomalie : ~2% dates incohérentes (fin avant début)
    if random.random() < 0.02:
        date_fin = date_debut - timedelta(days=random.randint(1, 5))

    absences.append({
        "absence_id": f"ABS{i:05d}",
        "enseignant_id": ens_id,
        "date_debut": date_debut,
        "date_fin": date_fin,
        "motif": random.choice(STATUTS_ABSENCE),
        "justifiee": random.choice(["Oui", "Non", "oui", "non", ""]),
    })


def write_csv(filename, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  -> {filename} : {len(rows)} lignes")


if __name__ == "__main__":
    print("Génération des données EduSmart - Source CSV (RH)")
    write_csv("departements.csv", departements)
    write_csv("enseignants.csv", enseignants)
    write_csv("salaires.csv", salaires)
    write_csv("absences.csv", absences)
    print("Terminé. Fichiers écrits dans:", OUT_DIR)
