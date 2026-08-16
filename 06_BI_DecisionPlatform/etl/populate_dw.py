"""
Peuple le schéma multidimensionnel (dimensions + faits) du Data Warehouse
à partir des tables de staging (stg_*) déjà chargées par le pipeline ETL.
"""

from sqlalchemy import create_engine, text
import pandas as pd
from config import DW_TARGET


def get_engine():
    url = (
        f"postgresql+psycopg2://{DW_TARGET['user']}:{DW_TARGET['password']}"
        f"@{DW_TARGET['host']}:{DW_TARGET['port']}/{DW_TARGET['dbname']}"
    )
    return create_engine(url)


def populate_dim_temps(engine):
    """Génère un calendrier couvrant les dates présentes dans les paiements et notes."""
    dates = pd.date_range(start="2022-01-01", end="2026-12-31", freq="D")
    df = pd.DataFrame({"date_complete": dates})
    df["jour"] = df["date_complete"].dt.day
    df["mois"] = df["date_complete"].dt.month
    df["nom_mois"] = df["date_complete"].dt.month_name()
    df["trimestre"] = df["date_complete"].dt.quarter
    df["annee"] = df["date_complete"].dt.year
    df["jour_semaine"] = df["date_complete"].dt.day_name()

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE dim_temps RESTART IDENTITY CASCADE"))
    df.to_sql("dim_temps", engine, if_exists="append", index=False)
    print(f"  -> dim_temps : {len(df)} lignes")


def populate_dim_etudiant(engine):
    df = pd.read_sql("SELECT * FROM stg_postgres_etudiants", engine)
    out = pd.DataFrame({
        "etudiant_id": df["etudiant_id"],
        "matricule": df.get("matricule"),
        "nom": df.get("nom"),
        "prenom": df.get("prenom"),
        "sexe": df.get("sexe"),
        "ville": df.get("ville"),
        "date_naissance": pd.to_datetime(df.get("date_naissance"), errors="coerce"),
        "date_inscription": pd.to_datetime(df.get("date_inscription"), errors="coerce"),
    })
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE dim_etudiant RESTART IDENTITY CASCADE"))
    out.to_sql("dim_etudiant", engine, if_exists="append", index=False)
    print(f"  -> dim_etudiant : {len(out)} lignes")


def populate_dim_formation(engine):
    classes = pd.read_sql("SELECT * FROM stg_postgres_classes", engine)

    out = pd.DataFrame({
        "classe_id": classes.get("classe_id"),
        "filiere": classes.get("filiere_id"),
        "classe": classes.get("nom_classe"),
    })
    out["cours"] = None
    out["module"] = None

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE dim_formation RESTART IDENTITY CASCADE"))
    out.to_sql("dim_formation", engine, if_exists="append", index=False)
    print(f"  -> dim_formation : {len(out)} lignes")


def populate_dim_enseignant(engine):
    df = pd.read_sql("SELECT * FROM stg_csv_enseignants", engine)
    out = pd.DataFrame({
        "enseignant_id": df.get("enseignant_id"),
        "nom": df.get("nom"),
        "prenom": df.get("prenom"),
        "diplome": df.get("diplome"),
        "type_contrat": df.get("type_contrat"),
        "departement_id": df.get("departement_id"),
    })
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE dim_enseignant RESTART IDENTITY CASCADE"))
    out.to_sql("dim_enseignant", engine, if_exists="append", index=False)
    print(f"  -> dim_enseignant : {len(out)} lignes")


def populate_dim_region(engine):
    df = pd.read_sql("SELECT DISTINCT ville FROM stg_postgres_etudiants WHERE ville IS NOT NULL", engine)
    df["departement"] = None
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE dim_region RESTART IDENTITY CASCADE"))
    df.to_sql("dim_region", engine, if_exists="append", index=False)
    print(f"  -> dim_region : {len(df)} lignes")


def populate_fait_paiements(engine):
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE fait_paiements RESTART IDENTITY"))
        conn.execute(text("""
            INSERT INTO fait_paiements (temps_id, etudiant_key, montant, mode_paiement)
            SELECT dt.temps_id, de.etudiant_key, p.montant, p.mode_paiement
            FROM stg_postgres_paiements p
            JOIN dim_etudiant de ON de.etudiant_id = p.etudiant_id
            JOIN dim_temps dt ON dt.date_complete = p.date_paiement::date
        """))
    count = pd.read_sql("SELECT COUNT(*) AS n FROM fait_paiements", engine)["n"][0]
    print(f"  -> fait_paiements : {count} lignes")


def populate_fait_notes(engine):
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE fait_notes RESTART IDENTITY"))
        conn.execute(text("""
            INSERT INTO fait_notes (temps_id, etudiant_key, note)
            SELECT dt.temps_id, de.etudiant_key, n.note_obtenue
            FROM stg_mysql_notes n
            JOIN dim_etudiant de ON de.etudiant_id = n.etudiant_id
            JOIN dim_temps dt ON dt.date_complete = n.date_passage::date
        """))
    count = pd.read_sql("SELECT COUNT(*) AS n FROM fait_notes", engine)["n"][0]
    print(f"  -> fait_notes : {count} lignes")


def run():
    engine = get_engine()

    print("Peuplement des dimensions...")
    populate_dim_temps(engine)
    populate_dim_etudiant(engine)
    populate_dim_formation(engine)
    populate_dim_enseignant(engine)
    populate_dim_region(engine)

    print("\nPeuplement des faits...")
    try:
        populate_fait_paiements(engine)
    except Exception as e:
        print(f"  ! fait_paiements : {e}")

    try:
        populate_fait_notes(engine)
    except Exception as e:
        print(f"  ! fait_notes : {e}")

    print("\nTerminé.")


if __name__ == "__main__":
    run()