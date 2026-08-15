"""
EduSmart - Source 5 : Redis - Plateforme temps réel
Ce script définit / documente la structure des clés Redis utilisées
pour représenter les données temporaires en temps réel de la plateforme.

Structure des clés :

1) session:{student_id}                (HASH)
   Champs : student_id, status, last_course, last_activity
   -> état de connexion courant de l'étudiant

2) active_sessions                     (SET)
   -> ensemble des student_id actuellement en ligne (pour compter les connectés)

3) progress:{student_id}:{course_id}   (STRING, valeur = pourcentage)
   -> progression en temps réel sur un cours donné

4) last_quiz:{student_id}              (HASH)
   Champs : quiz_id, score, timestamp
   -> dernier quiz réalisé par l'étudiant

5) notifications:{student_id}          (LIST)
   -> file de notifications en attente pour l'étudiant

Chaque clé "temporaire" possède une durée de vie (TTL) simulant le
caractère éphémère des données temps réel (sessions expirées, etc.).
Ce script se contente de FLUSH la base de test (db=1, dédiée EduSmart)
et de documenter le schéma ; les données elles-mêmes sont injectées
par insert_data.py (à partir de generate_data.py).
"""

import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1  # base dédiée EduSmart, isolée de la base par défaut (0)


def get_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def init_source():
    r = get_client()
    r.flushdb()
    print(f"Base Redis (db={REDIS_DB}) réinitialisée et prête pour EduSmart.")
    print("Structure des clés : session:{id} (HASH), active_sessions (SET),")
    print("progress:{id}:{course} (STRING), last_quiz:{id} (HASH), notifications:{id} (LIST)")


if __name__ == "__main__":
    init_source()
