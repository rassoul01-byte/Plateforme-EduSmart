"""
Extraction de la Source 4 (Logs mobile).
Priorité à une vraie instance MongoDB si MONGO_URI est définie ;
sinon, lecture du fichier JSONL local généré précédemment.
"""

import json
import pandas as pd
import os
from config import JSON_LOGS_PATH, MONGO_URI, MONGO_DB, MONGO_COLLECTION, STAGING_DIR


def extract_from_mongo():
    from pymongo import MongoClient

    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DB][MONGO_COLLECTION]
    docs = list(collection.find({}, {"_id": 0}))
    client.close()
    return pd.DataFrame(docs)


def extract_from_jsonl():
    records = []
    with open(JSON_LOGS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return pd.DataFrame(records)


def extract():
    if MONGO_URI:
        df = extract_from_mongo()
        print(f"  -> logs_mobile (MongoDB) : {len(df)} documents extraits")
    else:
        df = extract_from_jsonl()
        print(f"  -> logs_mobile (JSONL local) : {len(df)} événements extraits")

    output_path = os.path.join(STAGING_DIR, "mongo_logs_mobile.csv")
    df.to_csv(output_path, index=False)
    return {"logs_mobile": len(df)}


if __name__ == "__main__":
    print("Extraction Source 4 - Logs mobile (MongoDB / JSON)")
    result = extract()
    print("Terminé.", result)