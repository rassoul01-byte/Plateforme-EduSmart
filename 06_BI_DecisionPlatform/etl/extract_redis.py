"""
Extraction de la Source 5 (Redis - Temps réel)
"""

import redis
import pandas as pd
import os
import json
from config import REDIS_SOURCE, STAGING_DIR


def extract():
    r = redis.Redis(**REDIS_SOURCE, decode_responses=True)
    extracted = {}

    # Sessions (HASH session:{id})
    sessions = []
    for key in r.scan_iter("session:*"):
        data = r.hgetall(key)
        data["session_id"] = key.split(":")[1]
        sessions.append(data)
    df_sessions = pd.DataFrame(sessions)
    df_sessions.to_csv(os.path.join(STAGING_DIR, "redis_sessions.csv"), index=False)
    extracted["sessions"] = len(df_sessions)

    # Progress temps réel (STRING progress:{id}:{course})
    progress = []
    for key in r.scan_iter("progress:*"):
        parts = key.split(":")
        progress.append({
            "etudiant_id": parts[1] if len(parts) > 1 else None,
            "cours_id": parts[2] if len(parts) > 2 else None,
            "valeur": r.get(key),
        })
    df_progress = pd.DataFrame(progress)
    df_progress.to_csv(os.path.join(STAGING_DIR, "redis_progress.csv"), index=False)
    extracted["progress_realtime"] = len(df_progress)

    # Last quiz (HASH last_quiz:{id})
    quiz = []
    for key in r.scan_iter("last_quiz:*"):
        data = r.hgetall(key)
        data["etudiant_id"] = key.split(":")[1]
        quiz.append(data)
    df_quiz = pd.DataFrame(quiz)
    df_quiz.to_csv(os.path.join(STAGING_DIR, "redis_last_quiz.csv"), index=False)
    extracted["last_quiz"] = len(df_quiz)

    # Notifications (LIST notifications:{id})
    notifications = []
    for key in r.scan_iter("notifications:*"):
        etudiant_id = key.split(":")[1]
        for item in r.lrange(key, 0, -1):
            notifications.append({"etudiant_id": etudiant_id, "notification": item})
    df_notif = pd.DataFrame(notifications)
    df_notif.to_csv(os.path.join(STAGING_DIR, "redis_notifications.csv"), index=False)
    extracted["notifications"] = len(df_notif)

    for name, count in extracted.items():
        print(f"  -> {name} : {count} lignes extraites")

    return extracted


if __name__ == "__main__":
    print("Extraction Source 5 - Redis (Temps réel)")
    result = extract()
    print("Terminé.", result)