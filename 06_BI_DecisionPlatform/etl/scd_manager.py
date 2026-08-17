"""
Gestion SCD Type 2 pour dim_etudiant.
Détecte les changements sur les attributs suivis (actuellement : ville)
et crée une nouvelle version de la ligne plutôt que d'écraser l'ancienne.
"""

from sqlalchemy import text
import pandas as pd
from datetime import date

TRACKED_COLUMNS = ["ville"]  # attributs dont on veut suivre l'historique


def apply_scd2(engine):
    source = pd.read_sql("SELECT * FROM stg_postgres_etudiants", engine)
    today = date.today()

    with engine.begin() as conn:
        current = pd.read_sql(
            "SELECT * FROM dim_etudiant WHERE est_actuel = TRUE", conn
        )

        n_new = 0
        n_changed = 0
        n_unchanged = 0

        for _, row in source.iterrows():
            existing = current[current["etudiant_id"] == row["etudiant_id"]]

            if existing.empty:
                # Nouvel étudiant : première insertion
                conn.execute(text("""
                    INSERT INTO dim_etudiant
                        (etudiant_id, matricule, nom, prenom, sexe, ville,
                         date_naissance, date_inscription, date_debut, est_actuel)
                    VALUES
                        (:etudiant_id, :matricule, :nom, :prenom, :sexe, :ville,
                         :date_naissance, :date_inscription, :today, TRUE)
                """), {
                    "etudiant_id": row["etudiant_id"], "matricule": row.get("matricule"),
                    "nom": row.get("nom"), "prenom": row.get("prenom"),
                    "sexe": row.get("sexe"), "ville": row.get("ville"),
                    "date_naissance": row.get("date_naissance"),
                    "date_inscription": row.get("date_inscription"),
                    "today": today,
                })
                n_new += 1
                continue

            existing_row = existing.iloc[0]
            changed = any(
                str(existing_row[col]) != str(row.get(col)) for col in TRACKED_COLUMNS
            )

            if changed:
                # Clôture de l'ancienne version
                conn.execute(text("""
                    UPDATE dim_etudiant
                    SET date_fin = :today, est_actuel = FALSE
                    WHERE etudiant_key = :key
                """), {"today": today, "key": int(existing_row["etudiant_key"])})

                # Insertion de la nouvelle version
                conn.execute(text("""
                    INSERT INTO dim_etudiant
                        (etudiant_id, matricule, nom, prenom, sexe, ville,
                         date_naissance, date_inscription, date_debut, est_actuel)
                    VALUES
                        (:etudiant_id, :matricule, :nom, :prenom, :sexe, :ville,
                         :date_naissance, :date_inscription, :today, TRUE)
                """), {
                    "etudiant_id": row["etudiant_id"], "matricule": row.get("matricule"),
                    "nom": row.get("nom"), "prenom": row.get("prenom"),
                    "sexe": row.get("sexe"), "ville": row.get("ville"),
                    "date_naissance": row.get("date_naissance"),
                    "date_inscription": row.get("date_inscription"),
                    "today": today,
                })
                n_changed += 1
            else:
                n_unchanged += 1

    print(f"  -> dim_etudiant (SCD2) : {n_new} nouveaux, {n_changed} changements historisés, {n_unchanged} inchangés")