"""
Extraction de la Source 3 (CSV - Ressources Humaines)
"""

import pandas as pd
import os
from config import CSV_RH_PATH, STAGING_DIR

FILES = ["departements.csv", "enseignants.csv", "salaires.csv", "absences.csv"]


def extract():
    extracted = {}

    for filename in FILES:
        source_path = os.path.join(CSV_RH_PATH, filename)
        df = pd.read_csv(source_path)
        output_path = os.path.join(STAGING_DIR, f"csv_{filename}")
        df.to_csv(output_path, index=False)
        extracted[filename] = len(df)
        print(f"  -> {filename} : {len(df)} lignes extraites")

    return extracted


if __name__ == "__main__":
    print("Extraction Source 3 - CSV (RH)")
    result = extract()
    print("Terminé.", result)