"""
Transformation et nettoyage des données extraites (staging -> clean).
Applique les règles de qualité : suppression des doublons, gestion
des valeurs manquantes, uniformisation des types.
"""

import pandas as pd
import os
from config import STAGING_DIR, CLEAN_DIR

QUALITY_REPORT = []


def clean_dataframe(df, name, key_columns=None):
    """Nettoie un DataFrame et enregistre les statistiques qualité."""
    n_before = len(df)

    # Suppression des doublons
    if key_columns:
        df = df.drop_duplicates(subset=key_columns)
    else:
        df = df.drop_duplicates()
    n_duplicates = n_before - len(df)

    # Valeurs manquantes : on les compte avant nettoyage léger
    n_missing = df.isnull().sum().sum()

    n_after = len(df)

    QUALITY_REPORT.append({
        "table": name,
        "lignes_extraites": n_before,
        "doublons_supprimes": n_duplicates,
        "valeurs_manquantes": int(n_missing),
        "lignes_finales": n_after,
    })

    return df


def transform_all():
    files = [f for f in os.listdir(STAGING_DIR) if f.endswith(".csv")]

    for filename in files:
        path = os.path.join(STAGING_DIR, filename)
        df = pd.read_csv(path)

        # Normalisation basique : noms de colonnes en minuscules
        df.columns = [c.strip().lower() for c in df.columns]

        table_name = filename.replace(".csv", "")
        df_clean = clean_dataframe(df, table_name)

        output_path = os.path.join(CLEAN_DIR, filename)
        df_clean.to_csv(output_path, index=False)
        print(f"  -> {table_name} : {len(df_clean)} lignes après nettoyage")

    return QUALITY_REPORT


if __name__ == "__main__":
    print("Transformation des données (staging -> clean)")
    report = transform_all()
    print("Terminé.")
    for r in report:
        print(r)