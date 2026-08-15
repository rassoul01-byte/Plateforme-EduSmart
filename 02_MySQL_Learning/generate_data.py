"""
EduSmart - Source 2 : MySQL - Plateforme pédagogique
Génération de données réalistes (Faker) avec anomalies volontaires.

Sortie : fichiers CSV intermédiaires dans ./data/
  modules.csv, cours.csv, quiz.csv, notes.csv, progression.csv, temps_connexion.csv
"""

import csv
import os
import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker("fr_FR")
random.seed(7)
Faker.seed(7)

OUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT_DIR, exist_ok=True)

N_MODULES = 20
N_COURS = 120
N_QUIZ = 150
N_ETUDIANTS_RANGE = (1, 15150)  # doit chevaucher la source PostgreSQL (15000 + 150 doublons)
N_NOTES = 45000
N_PROGRESSION = 55000
N_CONNEXIONS = 70000

FILIERE_CODES = [f"FIL{str(i).zfill(3)}" for i in range(1, 16)]
TYPES_COURS = ["video", "pdf", "live", "article", "Video", "PDF"]  # casse incohérente
STATUTS_PROGRESSION = ["non_commence", "en_cours", "termine", "Termine", "EN_COURS", ""]
APPAREILS = ["Android", "iOS", "Web", "Desktop", "android", "IOS", ""]

# --------------------------------------------------------------------
# 1. Modules
# --------------------------------------------------------------------
modules = []
titres_modules = [
    "Algorithmique", "Bases de données", "Réseaux", "Programmation Web",
    "Data Mining", "Machine Learning", "Cybersécurité avancée", "UX/UI Design",
    "Gestion de projet", "Marketing digital", "Comptabilité générale",
    "Droit des affaires", "Anglais professionnel", "Statistiques",
    "Cloud Computing", "DevOps", "Mobile Development", "IoT",
    "Big Data", "Entrepreneuriat",
]
for i, titre in enumerate(titres_modules[:N_MODULES], start=1):
    modules.append({
        "module_id": i,
        "code_module": f"MOD{i:03d}",
        "titre": titre,
        "filiere_code": random.choice(FILIERE_CODES),
        "semestre": random.choice(["S1", "S2", "S3", "S4", "S5", "S6"]),
        "credits": random.choice([2, 3, 4, 5, 6]),
    })

# --------------------------------------------------------------------
# 2. Cours
# --------------------------------------------------------------------
cours = []
for i in range(1, N_COURS + 1):
    mod = random.choice(modules)
    pub = fake.date_between(start_date="-2y", end_date="today")
    duree = random.choice([10, 15, 20, 30, 45, 60, 90])
    # Anomalie : ~2% durées aberrantes (0 ou négatif)
    if random.random() < 0.02:
        duree = random.choice([0, -15])
    cours.append({
        "cours_id": i,
        "module_id": mod["module_id"],
        "titre_cours": f"{mod['titre']} - Partie {random.randint(1,8)}",
        "type_cours": random.choice(TYPES_COURS),
        "duree_minutes": duree,
        "date_publication": pub,
    })

# --------------------------------------------------------------------
# 3. Quiz
# --------------------------------------------------------------------
quiz = []
for i in range(1, N_QUIZ + 1):
    c = random.choice(cours)
    quiz.append({
        "quiz_id": i,
        "cours_id": c["cours_id"],
        "titre_quiz": f"Quiz - {c['titre_cours']}",
        "nb_questions": random.choice([5, 10, 15, 20]),
        "note_max": 20.00,
    })

# --------------------------------------------------------------------
# 4. Notes (avec anomalies)
# --------------------------------------------------------------------
notes = []
for i in range(1, N_NOTES + 1):
    q = random.choice(quiz)
    etu_id = random.randint(*N_ETUDIANTS_RANGE)
    note_val = round(random.uniform(0, 20), 2)
    # Anomalie : ~3% de notes hors barème (erreur de saisie)
    if random.random() < 0.03:
        note_val = round(random.uniform(21, 99), 2)
    # Anomalie : ~2% de notes manquantes
    note_final = "" if random.random() < 0.02 else note_val
    notes.append({
        "note_id": i,
        "etudiant_id": etu_id,
        "quiz_id": q["quiz_id"],
        "note_obtenue": note_final,
        "date_passage": fake.date_time_between(start_date="-2y", end_date="now"),
        "tentative": random.choice([1, 1, 1, 2, 3]),
    })

# Anomalie : doublons stricts (le même étudiant, même quiz, même tentative,
# enregistré deux fois -> double comptage possible dans le futur DW)
for _ in range(350):
    dup = random.choice(notes).copy()
    dup["note_id"] = len(notes) + 1
    notes.append(dup)

# --------------------------------------------------------------------
# 5. Progression (avec anomalies)
# --------------------------------------------------------------------
progression = []
for i in range(1, N_PROGRESSION + 1):
    c = random.choice(cours)
    pct = round(random.uniform(0, 100), 2)
    # Anomalie : ~2% de pourcentages hors bornes
    if random.random() < 0.02:
        pct = round(random.uniform(101, 150), 2)
    progression.append({
        "progression_id": i,
        "etudiant_id": random.randint(*N_ETUDIANTS_RANGE),
        "cours_id": c["cours_id"],
        "pourcentage_completion": pct,
        "statut": random.choice(STATUTS_PROGRESSION),
        "derniere_activite": fake.date_time_between(start_date="-1y", end_date="now"),
    })

# --------------------------------------------------------------------
# 6. Temps de connexion (avec anomalies)
# --------------------------------------------------------------------
temps_connexion = []
for i in range(1, N_CONNEXIONS + 1):
    duree = random.choice([5, 10, 20, 30, 45, 60, 90, 120])
    # Anomalie : ~1.5% de durées négatives/aberrantes (bug de tracking)
    if random.random() < 0.015:
        duree = random.choice([-5, 0, 999])
    temps_connexion.append({
        "session_id": i,
        "etudiant_id": random.randint(*N_ETUDIANTS_RANGE),
        "date_connexion": fake.date_between(start_date="-1y", end_date="today"),
        "heure_debut": fake.time(),
        "duree_minutes": duree,
        "appareil": random.choice(APPAREILS),
    })


def write_csv(filename, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  -> {filename} : {len(rows)} lignes")


if __name__ == "__main__":
    print("Génération des données EduSmart - Source MySQL (Learning)")
    write_csv("modules.csv", modules)
    write_csv("cours.csv", cours)
    write_csv("quiz.csv", quiz)
    write_csv("notes.csv", notes)
    write_csv("progression.csv", progression)
    write_csv("temps_connexion.csv", temps_connexion)
    print("Terminé. Fichiers écrits dans:", OUT_DIR)
