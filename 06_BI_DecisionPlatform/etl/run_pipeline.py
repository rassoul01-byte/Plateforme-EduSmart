"""
Orchestrateur du pipeline ETL complet EduSmart.
Extract -> Transform -> Load, sur les 5 sources, avec traçabilité complète.
"""

import time
import extract_postgres
import extract_mysql
import extract_csv
import extract_mongodb
import extract_redis
import transform
import load
import metadata_tracker as tracker


SOURCES = [
    ("postgres", extract_postgres),
    ("mysql", extract_mysql),
    ("csv_rh", extract_csv),
    ("logs_mobile", extract_mongodb),
    ("redis", extract_redis),
]


def run():
    start = time.time()
    tracker.ensure_metadata_tables()

    print("=== ÉTAPE 1 : EXTRACTION ===")
    for name, module in SOURCES:
        source_start = time.time()
        print(f"\nSource : {name}")
        try:
            result = module.extract()
            total_lignes = sum(result.values())
            duree = round(time.time() - source_start, 2)
            tracker.log_source_metadata(name, total_lignes, statut="succes")
            tracker.log_execution(name, duree, total_lignes, statut="succes")
        except Exception as e:
            duree = round(time.time() - source_start, 2)
            tracker.log_source_metadata(name, 0, statut="echec")
            tracker.log_execution(name, duree, 0, erreurs=str(e), statut="echec")
            print(f"  ERREUR sur {name} : {e}")

    print("\n=== ÉTAPE 2 : TRANSFORMATION ===")
    quality_report = transform.transform_all()

    print("\n=== ÉTAPE 3 : CHARGEMENT ===")
    load_result = load.load_all()

    duration = round(time.time() - start, 2)
    print(f"\nPipeline ETL terminé en {duration}s")
    print(f"Tables chargées dans le DW : {len(load_result)}")

    return {"quality_report": quality_report, "load_result": load_result, "duration": duration}


if __name__ == "__main__":
    run()