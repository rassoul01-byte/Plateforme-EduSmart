"""
EduSmart - Source 5 : Redis - Plateforme temps réel
Insertion du dataset généré (data/redis_dataset.json) dans Redis,
selon la structure de clés documentée dans create_source.py.
"""

import json
import os
import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "redis_dataset.json")


def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

    with open(DATA_PATH, encoding="utf-8") as f:
        dataset = json.load(f)

    # 1) sessions -> HASH session:{id} + SET active_sessions
    for s in dataset["sessions"]:
        key = f"session:{s['student_id']}"
        mapping = {k: v for k, v in s.items() if k not in ("student_id", "ttl_seconds")}
        mapping["student_id"] = s["student_id"]
        r.hset(key, mapping=mapping)
        r.expire(key, s.get("ttl_seconds", 1800))
        if s.get("status") in ("online", "en_ligne", "ONLINE"):
            r.sadd("active_sessions", s["student_id"])
    print(f"sessions insérées : {len(dataset['sessions'])}")

    # 2) progression temps réel -> STRING progress:{student}:{course}
    for p in dataset["progress_realtime"]:
        key = f"progress:{p['student_id']}:{p['course_id']}"
        r.set(key, p["pourcentage"], ex=3600)
    print(f"progress_realtime insérées : {len(dataset['progress_realtime'])}")

    # 3) derniers quiz -> HASH last_quiz:{id}
    for q in dataset["last_quiz"]:
        key = f"last_quiz:{q['student_id']}"
        r.hset(key, mapping={"quiz_id": q["quiz_id"], "score": q["score"], "timestamp": q["timestamp"]})
    print(f"last_quiz insérées : {len(dataset['last_quiz'])}")

    # 4) notifications -> LIST notifications:{id}
    for n in dataset["notifications"]:
        key = f"notifications:{n['student_id']}"
        if n["messages"]:
            r.rpush(key, *n["messages"])
    print(f"notifications insérées pour {len(dataset['notifications'])} étudiants")

    print("Insertion terminée avec succès.")
    print("Nombre de sessions actives (SET active_sessions):", r.scard("active_sessions"))


if __name__ == "__main__":
    main()
