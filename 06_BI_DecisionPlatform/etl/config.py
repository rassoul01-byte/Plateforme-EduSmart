"""
Configuration centralisée des connexions aux 5 sources EduSmart
et à la base cible du Data Warehouse.
"""

import os

# --- Sources opérationnelles ---
POSTGRES_SOURCE = {
    "host": "127.0.0.1",
    "port": 5432,
    "dbname": "edusmart_academic",
    "user": "postgres",
    "password": "postgres",
}

MYSQL_SOURCE = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "edusmart_learning",
    "user": "root",
    "password": "root",
}

REDIS_SOURCE = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 1,
}

# Chemin vers les fichiers CSV RH (Source 3)
CSV_RH_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "03_CSV_RH"
)

# Chemin vers les logs mobile (Source 4).
# Si une vraie instance MongoDB est disponible, MONGO_URI peut être utilisée
# à la place du fichier JSONL local.
JSON_LOGS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "04_JSON_Logs", "logs_mobile.jsonl"
)
MONGO_URI = os.environ.get("MONGO_URI", None)  # ex: "mongodb://localhost:27017"
MONGO_DB = "edusmart_logs"
MONGO_COLLECTION = "logs_mobile"

# --- Dossiers du pipeline ETL ---
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data_warehouse")
STAGING_DIR = os.path.join(BASE_DIR, "staging")   # données extraites brutes
CLEAN_DIR = os.path.join(BASE_DIR, "clean")       # données transformées/propres

os.makedirs(STAGING_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)

# --- Base cible du Data Warehouse ---
DW_TARGET = {
    "host": "127.0.0.1",
    "port": 5432,
    "dbname": "edusmart_dw",
    "user": "postgres",
    "password": "postgres",
}