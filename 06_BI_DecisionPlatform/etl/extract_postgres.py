"""
Extraction de la Source 1 (PostgreSQL - Académique)
"""

import psycopg2
import pandas as pd
import os
from config import POSTGRES_SOURCE, STAGING_DIR

TABLES = ["filieres", "classes", "etudiants", "inscriptions", "paiements"]


def extract():
    conn = psycopg2.connect(**POSTGRES_SOURCE)
    extracted = {}

    for table in TABLES:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        output_path = os.path.join(STAGING_DIR, f"postgres_{table}.csv")
        df.to_csv(output_path, index=False)
        extracted[table] = len(df)
        print(f"  -> {table} : {len(df)} lignes extraites")

    conn.close()
    return extracted


if __name__ == "__main__":
    print("Extraction Source 1 - PostgreSQL (Académique)")
    result = extract()
    print("Terminé.", result)