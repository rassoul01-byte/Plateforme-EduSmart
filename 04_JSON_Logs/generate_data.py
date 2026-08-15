"""
EduSmart - Source 4 : JSON - Journaux de l'application mobile
Génération d'un flux d'événements utilisateurs (plusieurs milliers),
tel qu'il serait produit par l'application mobile et stocké
(fichiers JSON Lines / logs bruts), avec anomalies volontaires.

Sortie :
  - logs_mobile.json       (tableau JSON complet)
  - logs_mobile.jsonl      (1 événement JSON par ligne, format "log réel")
"""

import json
import os
import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker("fr_FR")
random.seed(99)
Faker.seed(99)

OUT_DIR = os.path.dirname(__file__)

N_EVENTS = 112000
N_ETUDIANTS_RANGE = (1, 15150)  # chevauche volontairement la source PostgreSQL

EVENTS = [
    "App Opened", "Login", "Logout", "Course Viewed", "Quiz Started",
    "Quiz Completed", "Video Played", "Video Paused", "Notification Received",
    "quiz_started", "QUIZ_COMPLETED",       # anomalie : casse / format incohérent
]
DEVICES = ["Android", "iOS", "android", "IOS", "Web", ""]
VILLES = ["Dakar", "Thies", "Saint-Louis", "Ziguinchor", "Kaolack",
          "Touba", "Mbour", None, ""]


def random_timestamp():
    dt = fake.date_time_between(start_date="-1y", end_date="now")
    # Anomalie : ~5% de timestamps dans un format différent (pas ISO)
    if random.random() < 0.05:
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    return dt.isoformat()


events = []
for i in range(1, N_EVENTS + 1):
    student_id = random.randint(*N_ETUDIANTS_RANGE)
    # Anomalie : ~2% de student_id manquant (null) -> événement anonyme mal tracké
    if random.random() < 0.02:
        student_id = None

    event = {
        "event_id": f"evt_{i:06d}",
        "student_id": student_id,
        "event": random.choice(EVENTS),
        "device": random.choice(DEVICES),
        "city": random.choice(VILLES),
        "timestamp": random_timestamp(),
    }

    # Anomalie : ~3% d'événements avec un champ additionnel imprévu
    # (schéma non strict, cohérent avec une source NoSQL/JSON réelle)
    if random.random() < 0.03:
        event["app_version"] = random.choice(["3.2.1", "3.1.0", "4.0.0-beta"])

    # Anomalie : ~1% de doublons exacts (retransmission réseau côté mobile)
    events.append(event)
    if random.random() < 0.01:
        events.append(dict(event))

# Anomalie : quelques événements avec des clés manquantes (event ou device absent)
for _ in range(280):
    e = dict(random.choice(events))
    e["event_id"] = f"evt_bad_{random.randint(1000,9999)}"
    e.pop("device", None)
    events.append(e)

if __name__ == "__main__":
    print("Génération des données EduSmart - Source JSON (Logs mobile)")

    path_json = os.path.join(OUT_DIR, "logs_mobile.json")
    with open(path_json, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2, default=str)
    print(f"  -> logs_mobile.json : {len(events)} événements")

    path_jsonl = os.path.join(OUT_DIR, "logs_mobile.jsonl")
    with open(path_jsonl, "w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e, ensure_ascii=False, default=str) + "\n")
    print(f"  -> logs_mobile.jsonl : {len(events)} lignes")
    print("Terminé.")
