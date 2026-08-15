"""
Orchestrateur du pipeline ETL complet EduSmart.
Extract -> Transform -> Load, sur les 5 sources.
"""

import time
import extract_postgres
import extract_mysql
import extract_csv
import extract_mongodb
import extract_redis
import transform
import load


def run():
    start = time.time()

    print("=== ÉTAPE 1 : EXTRACTION ===")
    print("\nSource 1 - PostgreSQL")
    extract_postgres.extract()
    print("\nSource 2 - MySQL")
    extract_mysql.extract()
    print("\nSource 3 - CSV (RH)")
    extract_csv.extract()
    print("\nSource 4 - Logs mobile")
    extract_mongodb.extract()
    print("\nSource 5 - Redis")
    extract_redis.extract()

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