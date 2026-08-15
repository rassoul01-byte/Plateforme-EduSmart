"""
Extraction de la Source 2 (MySQL - Learning)
"""

import mysql.connector
import pandas as pd
import os
from config import MYSQL_SOURCE, STAGING_DIR

TABLES = ["modules", "cours", "quiz", "notes", "progression", "temps_connexion"]


def extract():
    conn = mysql.connector.connect(**MYSQL_SOURCE)
    extracted = {}

    for table in TABLES:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        output_path = os.path.join(STAGING_DIR, f"mysql_{table}.csv")
        df.to_csv(output_path, index=False)
        extracted[table] = len(df)
        print(f"  -> {table} : {len(df)} lignes extraites")

    conn.close()
    return extracted


if __name__ == "__main__":
    print("Extraction Source 2 - MySQL (Learning)")
    result = extract()
    print("Terminé.", result)