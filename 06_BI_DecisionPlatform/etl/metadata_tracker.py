"""
Gestion des métadonnées et de la traçabilité du pipeline ETL EduSmart.
Crée et alimente deux tables dans le Data Warehouse :
- metadata_sources : état courant de chaque source
- etl_execution_log : historique de toutes les exécutions du pipeline
"""

import psycopg2
from datetime import datetime
from config import DW_TARGET

PIPELINE_VERSION = "1.0"


def get_connection():
    return psycopg2.connect(
        host=DW_TARGET["host"],
        port=DW_TARGET["port"],
        dbname=DW_TARGET["dbname"],
        user=DW_TARGET["user"],
        password=DW_TARGET["password"],
    )


def ensure_metadata_tables():
    """Crée les tables de métadonnées si elles n'existent pas déjà."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS metadata_sources (
            source VARCHAR(100) PRIMARY KEY,
            derniere_extraction TIMESTAMP,
            version VARCHAR(20),
            nombre_lignes INTEGER,
            statut VARCHAR(20)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS etl_execution_log (
            id SERIAL PRIMARY KEY,
            source VARCHAR(100),
            date_execution TIMESTAMP,
            duree_secondes NUMERIC,
            nombre_lignes INTEGER,
            erreurs TEXT,
            statut VARCHAR(20)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def log_source_metadata(source, nombre_lignes, statut="succes"):
    """Met à jour l'état courant d'une source (upsert)."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO metadata_sources (source, derniere_extraction, version, nombre_lignes, statut)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (source) DO UPDATE SET
            derniere_extraction = EXCLUDED.derniere_extraction,
            version = EXCLUDED.version,
            nombre_lignes = EXCLUDED.nombre_lignes,
            statut = EXCLUDED.statut;
    """, (source, datetime.now(), PIPELINE_VERSION, nombre_lignes, statut))

    conn.commit()
    cur.close()
    conn.close()


def log_execution(source, duree_secondes, nombre_lignes, erreurs=None, statut="succes"):
    """Ajoute une ligne dans l'historique d'exécution (jamais écrasé)."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO etl_execution_log (source, date_execution, duree_secondes, nombre_lignes, erreurs, statut)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (source, datetime.now(), duree_secondes, nombre_lignes, erreurs, statut))

    conn.commit()
    cur.close()
    conn.close()