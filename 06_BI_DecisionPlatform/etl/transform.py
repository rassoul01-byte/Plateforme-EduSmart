"""
Transformation et nettoyage des données extraites (staging -> clean).
Applique les règles de qualité : suppression des doublons, gestion
des valeurs manquantes, détection d'incohérences, uniformisation des types.
Produit un rapport qualité complet dans quality_reports/.
"""

import pandas as pd
import os
import json
from datetime import datetime
from config import STAGING_DIR, CLEAN_DIR

QUALITY_REPORT = []

# Règles d'incohérence simples par table (colonne -> condition invalide)
INCONSISTENCY_RULES = {
    "postgres_paiements": {"montant": lambda s: s < 0},
    "mysql_notes": {"note": lambda s: (s < 0) | (s > 20)},
    "postgres_etudiants": {"email": lambda s: s.isna() | (s == "")},
}


def detect_inconsistencies(df, table_name):
    """Détecte les lignes incohérentes selon les règles définies, sans les supprimer."""
    rules = INCONSISTENCY_RULES.get(table_name, {})
    total_incoherences = 0

    for column, condition in rules.items():
        if column in df.columns:
            try:
                mask = condition(df[column])
                total_incoherences += int(mask.sum())
            except Exception:
                pass

    return total_incoherences


def clean_dataframe(df, name, key_columns=None):
    """Nettoie un DataFrame et enregistre les statistiques qualité."""
    n_before = len(df)

    if key_columns:
        df = df.drop_duplicates(subset=key_columns)
    else:
        df = df.drop_duplicates()
    n_duplicates = n_before - len(df)

    n_missing = int(df.isnull().sum().sum())
    n_incoherences = detect_inconsistencies(df, name)

    # Corrections automatiques simples : on comble les valeurs manquantes
    # textuelles par "inconnu" et les numériques par 0, en traçant le nombre
    # de corrections effectuées.
    n_corrections = 0
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype == object:
                n_corrections += int(df[col].isnull().sum())
                df[col] = df[col].fillna("inconnu")
            else:
                n_corrections += int(df[col].isnull().sum())
                df[col] = df[col].fillna(0)

    n_after = len(df)
    n_rejected = 0  # aucune ligne rejetée dans cette version, tout est corrigé/conservé

    QUALITY_REPORT.append({
        "table": name,
        "lignes_extraites": n_before,
        "lignes_rejetees": n_rejected,
        "doublons_supprimes": n_duplicates,
        "valeurs_manquantes": n_missing,
        "incoherences_detectees": n_incoherences,
        "corrections_effectuees": n_corrections,
        "lignes_finales": n_after,
    })

    return df


def transform_all():
    files = [f for f in os.listdir(STAGING_DIR) if f.endswith(".csv")]

    for filename in files:
        path = os.path.join(STAGING_DIR, filename)
        table_name = filename.replace(".csv", "")

        if os.path.getsize(path) == 0:
            print(f"  -> {table_name} : fichier vide, ignoré")
            QUALITY_REPORT.append({
                "table": table_name, "lignes_extraites": 0, "lignes_rejetees": 0,
                "doublons_supprimes": 0, "valeurs_manquantes": 0,
                "incoherences_detectees": 0, "corrections_effectuees": 0,
                "lignes_finales": 0,
            })
            continue

        try:
            df = pd.read_csv(path)
        except pd.errors.EmptyDataError:
            print(f"  -> {table_name} : aucune colonne/donnée, ignoré")
            QUALITY_REPORT.append({
                "table": table_name, "lignes_extraites": 0, "lignes_rejetees": 0,
                "doublons_supprimes": 0, "valeurs_manquantes": 0,
                "incoherences_detectees": 0, "corrections_effectuees": 0,
                "lignes_finales": 0,
            })
            continue

        df.columns = [c.strip().lower() for c in df.columns]
        df_clean = clean_dataframe(df, table_name)

        output_path = os.path.join(CLEAN_DIR, filename)
        df_clean.to_csv(output_path, index=False)
        print(f"  -> {table_name} : {len(df_clean)} lignes après nettoyage")

    save_quality_report()
    return QUALITY_REPORT


def save_quality_report():
    """Sauvegarde le rapport qualité en CSV et en Markdown lisible."""
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "quality_reports")
    os.makedirs(reports_dir, exist_ok=True)

    df_report = pd.DataFrame(QUALITY_REPORT)
    csv_path = os.path.join(reports_dir, "rapport_qualite.csv")
    df_report.to_csv(csv_path, index=False)

    md_path = os.path.join(reports_dir, "rapport_qualite.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Rapport qualité — EduSmart\n\n")
        f.write(f"Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| Table | Extraites | Rejetées | Doublons | Manquantes | Incohérences | Corrections | Finales |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for r in QUALITY_REPORT:
            f.write(
                f"| {r['table']} | {r['lignes_extraites']} | {r['lignes_rejetees']} | "
                f"{r['doublons_supprimes']} | {r['valeurs_manquantes']} | "
                f"{r['incoherences_detectees']} | {r['corrections_effectuees']} | "
                f"{r['lignes_finales']} |\n"
            )

    print(f"\nRapport qualité sauvegardé : {csv_path} et {md_path}")


if __name__ == "__main__":
    print("Transformation des données (staging -> clean)")
    report = transform_all()
    print("Terminé.")