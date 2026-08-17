"""
Fusionne les exports CSV du Data Warehouse EduSmart en un seul
classeur Excel multi-onglets, prêt à être importé dans Power BI.
"""

import pandas as pd
import os

EXPORT_DIR = os.path.dirname(__file__)
OUTPUT_FILE = os.path.join(EXPORT_DIR, "EduSmart_DW.xlsx")

TABLES = {
    "dim_temps": "dim_temps.csv",
    "dim_etudiant": "dim_etudiant.csv",
    "dim_formation": "dim_formation.csv",
    "dim_enseignant": "dim_enseignant.csv",
    "dim_region": "dim_region.csv",
    "fait_paiements": "fait_paiements.csv",
    "fait_notes": "fait_notes.csv",
}


def build():
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        for sheet_name, filename in TABLES.items():
            path = os.path.join(EXPORT_DIR, filename)
            df = pd.read_csv(path)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"  -> {sheet_name} : {len(df)} lignes ajoutées")

    print(f"\nClasseur créé : {OUTPUT_FILE}")


if __name__ == "__main__":
    build()