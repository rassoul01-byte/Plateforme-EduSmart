"""
Chargement des données nettoyées dans le Data Warehouse (PostgreSQL).
Crée la base cible si nécessaire, puis charge chaque fichier "clean"
dans une table de staging du DW (schéma final en étoile : Phase 7-8).
"""

import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import os
from config import DW_TARGET, CLEAN_DIR


def ensure_database_exists():
    conn = psycopg2.connect(
        host=DW_TARGET["host"],
        port=DW_TARGET["port"],
        dbname="postgres",
        user=DW_TARGET["user"],
        password=DW_TARGET["password"],
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DW_TARGET["dbname"],))
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {DW_TARGET['dbname']}")
        print(f"Base '{DW_TARGET['dbname']}' créée.")
    else:
        print(f"Base '{DW_TARGET['dbname']}' déjà existante.")
    cur.close()
    conn.close()


def load_all():
    ensure_database_exists()

    url = (
        f"postgresql+psycopg2://{DW_TARGET['user']}:{DW_TARGET['password']}"
        f"@{DW_TARGET['host']}:{DW_TARGET['port']}/{DW_TARGET['dbname']}"
    )
    engine = create_engine(url)

    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith(".csv")]
    loaded = {}

    for filename in files:
        table_name = "stg_" + filename.replace(".csv", "")
        df = pd.read_csv(os.path.join(CLEAN_DIR, filename))
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        loaded[table_name] = len(df)
        print(f"  -> {table_name} : {len(df)} lignes chargées")

    return loaded


if __name__ == "__main__":
    print("Chargement dans le Data Warehouse (edusmart_dw)")
    result = load_all()
    print("Terminé.", result)