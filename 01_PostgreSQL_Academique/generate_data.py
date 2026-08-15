"""
EduSmart - Source 1 : PostgreSQL - Gestion Académique
Génération de données réalistes (Faker) avec anomalies volontaires.

Sortie : fichiers CSV intermédiaires dans ./data/
  - filieres.csv
  - classes.csv
  - etudiants.csv
  - inscriptions.csv
  - paiements.csv

Ces CSV représentent l'extraction brute de la source telle qu'elle
serait récupérée par l'équipe décisionnelle (avant nettoyage ETL).
"""

import csv
import os
import random
import uuid
from datetime import datetime, timedelta

from faker import Faker

fake = Faker("fr_FR")
random.seed(42)
Faker.seed(42)

OUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------------------------
# Paramètres de volumétrie
# --------------------------------------------------------------------
N_FILIERES = 15
N_CLASSES = 220
N_ETUDIANTS = 15000
N_INSCRIPTIONS = 18000
N_PAIEMENTS = 30000

NIVEAUX = ["Licence", "Master", "Bachelor", "BTS"]
VILLES = ["Dakar", "Thiès", "Saint-Louis", "Ziguinchor", "Kaolack",
          "Touba", "Rufisque", "Mbour", "Diourbel", None]  # None -> valeur manquante
SEXES_VALIDES = ["M", "F"]
SEXES_SALES = ["M", "F", "Homme", "Femme", "H", "m", "f", ""]  # erreurs de saisie / casse
MODES_PAIEMENT = ["Especes", "especes", "Mobile Money", "mobile_money",
                   "Virement", "virement bancaire", "Cheque", "carte"]
STATUTS_PAIEMENT = ["paye", "Paye", "en_attente", "En attente", "echoue", "rembourse"]
STATUTS_INSCRIPTION = ["active", "Active", "terminee", "abandonnee", "en_attente"]


def phone_format():
    """Génère des numéros dans des formats hétérogènes (anomalie de format)."""
    n = fake.msisdn()[-9:]
    fmt = random.choice([0, 1, 2, 3])
    if fmt == 0:
        return f"+221{n}"
    if fmt == 1:
        return f"77{n[2:]}"
    if fmt == 2:
        return f"{n[:2]}-{n[2:4]}-{n[4:6]}-{n[6:8]}"
    return n  # brut, sans indicatif


def matricule_format(i):
    """La majorité suit un format standard, une minorité un format legacy incompatible."""
    if random.random() < 0.92:
        return f"ETU{2019 + (i % 7)}{i:04d}"
    else:
        return str(1000000 + i)  # ancien système, format numérique brut (source de conflit d'ID)


# --------------------------------------------------------------------
# 1. Filières
# --------------------------------------------------------------------
filieres = []
noms_filieres = [
    "Informatique de Gestion", "Génie Logiciel", "Réseaux et Télécoms",
    "Data Science", "Cybersécurité", "Marketing Digital", "Finance Comptabilité",
    "Ressources Humaines", "Commerce International", "Génie Civil",
    "Électromécanique", "Communication", "Logistique et Transport",
    "Intelligence Artificielle", "Design Numérique",
]
for i, nom in enumerate(noms_filieres[:N_FILIERES], start=1):
    filieres.append({
        "filiere_id": i,
        "code_filiere": f"FIL{i:03d}",
        "nom_filiere": nom,
        "niveau": random.choice(NIVEAUX),
        "duree_annees": random.choice([2, 3, 5]),
        "responsable": fake.name(),
        "date_creation": fake.date_between(start_date="-10y", end_date="-1y"),
    })

# --------------------------------------------------------------------
# 2. Classes
# --------------------------------------------------------------------
classes = []
for i in range(1, N_CLASSES + 1):
    fil = random.choice(filieres)
    classes.append({
        "classe_id": i,
        "filiere_id": fil["filiere_id"],
        "nom_classe": f"{fil['code_filiere']}-{random.choice(['A','B','C'])}{random.randint(1,3)}",
        "annee_scolaire": random.choice(["2023-2024", "2024-2025", "2025-2026"]),
        "effectif_max": random.choice([25, 30, 35, 40]),
        "salle": f"Salle {random.randint(100, 320)}",
    })

# --------------------------------------------------------------------
# 3. Étudiants (avec anomalies)
# --------------------------------------------------------------------
etudiants = []
duplicate_emails = {}
for i in range(1, N_ETUDIANTS + 1):
    prenom = fake.first_name()
    nom = fake.last_name()
    date_naissance = fake.date_of_birth(minimum_age=17, maximum_age=28)
    date_inscription = fake.date_between(start_date="-3y", end_date="today")

    # Anomalie : ~3% des dates de naissance incohérentes (après la date d'inscription)
    if random.random() < 0.03:
        date_naissance = date_inscription + timedelta(days=random.randint(30, 900))

    email = f"{prenom.lower()}.{nom.lower()}{random.randint(1,99)}@gmail.com"
    # Anomalie : ~4% d'emails dupliqués volontairement
    if random.random() < 0.04 and duplicate_emails:
        email = random.choice(list(duplicate_emails.values()))
    else:
        duplicate_emails[i] = email

    etudiants.append({
        "etudiant_id": i,
        "matricule": matricule_format(i),
        "nom": nom.upper() if random.random() < 0.3 else nom,  # casse incohérente
        "prenom": prenom,
        "date_naissance": date_naissance,
        # Anomalie : sexe mal standardisé
        "sexe": random.choice(SEXES_SALES),
        # Anomalie : ~6% d'emails manquants
        "email": "" if random.random() < 0.06 else email,
        # Anomalie : ~8% de téléphones manquants, formats hétérogènes sinon
        "telephone": "" if random.random() < 0.08 else phone_format(),
        # Anomalie : ~5% de villes manquantes (None -> vide)
        "ville": random.choice(VILLES) or "",
        "date_inscription": date_inscription,
        "classe_id": random.choice(classes)["classe_id"],
    })

# Anomalie : quelques doublons stricts d'étudiants (même matricule ré-inséré) - ~1%
for _ in range(150):
    dup = random.choice(etudiants).copy()
    dup["etudiant_id"] = len(etudiants) + 1
    etudiants.append(dup)

# --------------------------------------------------------------------
# 4. Inscriptions
# --------------------------------------------------------------------
inscriptions = []
for i in range(1, N_INSCRIPTIONS + 1):
    etu = random.choice(etudiants)
    classe = random.choice(classes)
    inscriptions.append({
        "inscription_id": i,
        "etudiant_id": etu["etudiant_id"],
        "filiere_id": classe["filiere_id"],
        "classe_id": classe["classe_id"],
        "annee_scolaire": classe["annee_scolaire"],
        "date_inscription": fake.date_between(start_date="-3y", end_date="today"),
        "statut": random.choice(STATUTS_INSCRIPTION),
    })

# --------------------------------------------------------------------
# 5. Paiements (avec enregistrements orphelins)
# --------------------------------------------------------------------
paiements = []
max_etu_id = max(e["etudiant_id"] for e in etudiants)
max_insc_id = max(i["inscription_id"] for i in inscriptions)
for i in range(1, N_PAIEMENTS + 1):
    insc = random.choice(inscriptions)
    montant = round(random.uniform(20000, 350000), 2)
    # Anomalie : ~2% de montants négatifs / aberrants (erreur de saisie)
    if random.random() < 0.02:
        montant = -montant

    etudiant_id = insc["etudiant_id"]
    inscription_id = insc["inscription_id"]
    # Anomalie : ~2% d'enregistrements orphelins (référencent un id inexistant)
    if random.random() < 0.02:
        etudiant_id = max_etu_id + random.randint(1, 50)
        inscription_id = max_insc_id + random.randint(1, 50)

    paiements.append({
        "paiement_id": i,
        "etudiant_id": etudiant_id,
        "inscription_id": inscription_id,
        "montant": montant,
        "devise": random.choice(["XOF", "XOF", "XOF", "EUR"]),
        "mode_paiement": random.choice(MODES_PAIEMENT),
        "date_paiement": fake.date_time_between(start_date="-3y", end_date="now"),
        "statut_paiement": random.choice(STATUTS_PAIEMENT),
    })


def write_csv(filename, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  -> {filename} : {len(rows)} lignes")


if __name__ == "__main__":
    print("Génération des données EduSmart - Source PostgreSQL (Académique)")
    write_csv("filieres.csv", filieres)
    write_csv("classes.csv", classes)
    write_csv("etudiants.csv", etudiants)
    write_csv("inscriptions.csv", inscriptions)
    write_csv("paiements.csv", paiements)
    print("Terminé. Fichiers écrits dans:", OUT_DIR)
