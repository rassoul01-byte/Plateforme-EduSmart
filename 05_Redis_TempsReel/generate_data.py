"""
EduSmart - Source 5 : Redis - Plateforme temps réel
Génération de données temps réel réalistes (Faker) avec anomalies
volontaires, exportées en JSON intermédiaire (data/redis_dataset.json)
avant insertion effective dans Redis par insert_data.py.
"""

import json
import os
import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker("fr_FR")
random.seed(55)
Faker.seed(55)

OUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT_DIR, exist_ok=True)

N_ETUDIANTS_RANGE = (1, 15150)
N_SESSIONS = 5600         # étudiants "actuellement actifs" simulés
N_NOTIFICATIONS_USERS = 2800

STATUTS = ["online", "offline", "idle", "ONLINE", "en_ligne", ""]  # anomalie : non standardisé

sessions = []
used_ids = set()
for _ in range(N_SESSIONS):
    student_id = random.randint(*N_ETUDIANTS_RANGE)
    used_ids.add(student_id)
    last_activity = datetime.now() - timedelta(minutes=random.randint(0, 600))

    entry = {
        "student_id": student_id,
        "status": random.choice(STATUTS),
        "last_course": random.randint(1, 120),
        # Anomalie : ~4% de last_activity au format différent
        "last_activity": (
            last_activity.strftime("%d/%m/%Y %H:%M")
            if random.random() < 0.04
            else last_activity.strftime("%Y-%m-%d %H:%M:%S")
        ),
        "ttl_seconds": random.choice([300, 600, 1800, 3600]),
    }
    # Anomalie : ~3% de champs manquants (last_course absent)
    if random.random() < 0.03:
        entry.pop("last_course", None)
    sessions.append(entry)

# progression temps réel par étudiant/cours
progress_realtime = []
for _ in range(7500):
    pct = round(random.uniform(0, 100), 1)
    if random.random() < 0.02:
        pct = round(random.uniform(101, 130), 1)  # anomalie : hors bornes
    progress_realtime.append({
        "student_id": random.randint(*N_ETUDIANTS_RANGE),
        "course_id": random.randint(1, 120),
        "pourcentage": pct,
    })

# derniers quiz réalisés
last_quiz = []
for sid in random.sample(range(*N_ETUDIANTS_RANGE), 3500):
    last_quiz.append({
        "student_id": sid,
        "quiz_id": random.randint(1, 150),
        "score": round(random.uniform(0, 20), 1),
        "timestamp": (datetime.now() - timedelta(hours=random.randint(0, 72))).isoformat(),
    })

# notifications en attente (listes, taille variable)
notifications = []
for _ in range(N_NOTIFICATIONS_USERS):
    sid = random.randint(*N_ETUDIANTS_RANGE)
    # Anomalie : ~3% référencent un étudiant hors plage connue (orphelin)
    if random.random() < 0.03:
        sid = 15150 + random.randint(1, 300)
    msgs = [fake.sentence(nb_words=6) for _ in range(random.randint(0, 5))]
    notifications.append({"student_id": sid, "messages": msgs})

dataset = {
    "sessions": sessions,
    "progress_realtime": progress_realtime,
    "last_quiz": last_quiz,
    "notifications": notifications,
}

if __name__ == "__main__":
    print("Génération des données EduSmart - Source Redis (temps réel)")
    path = os.path.join(OUT_DIR, "redis_dataset.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2, default=str)
    print(f"  -> sessions : {len(sessions)}")
    print(f"  -> progress_realtime : {len(progress_realtime)}")
    print(f"  -> last_quiz : {len(last_quiz)}")
    print(f"  -> notifications : {len(notifications)}")
    print("Terminé. Fichier écrit :", path)
