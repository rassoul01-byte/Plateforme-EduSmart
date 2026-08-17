"""
Suite de tests de validation du pipeline ETL EduSmart.
Vérifie : complétude de l'extraction, complétude du chargement,
absence de perte de données, absence d'erreurs, validité des clés.
"""

from sqlalchemy import text, create_engine
import pandas as pd
from config import DW_TARGET

EXPECTED_MIN_ROWS = {
    "stg_postgres_etudiants": 15000,
    "stg_postgres_inscriptions": 17000,
    "stg_postgres_paiements": 29000,
    "stg_mysql_notes": 45000,
    "stg_mysql_progression": 54000,
    "stg_csv_enseignants": 400,
}

FK_CHECKS = [
    ("fait_paiements", "etudiant_key", "dim_etudiant", "etudiant_key"),
    ("fait_notes", "etudiant_key", "dim_etudiant", "etudiant_key"),
]


def get_engine():
    url = (
        f"postgresql+psycopg2://{DW_TARGET['user']}:{DW_TARGET['password']}"
        f"@{DW_TARGET['host']}:{DW_TARGET['port']}/{DW_TARGET['dbname']}"
    )
    return create_engine(url)


def test_1_completude_extraction(engine):
    print("\n[Test 1] Complétude de l'extraction")
    all_ok = True
    for table, min_rows in EXPECTED_MIN_ROWS.items():
        try:
            count = pd.read_sql(text(f"SELECT COUNT(*) AS n FROM {table}"), engine)["n"][0]
            status = "OK" if count >= min_rows else "ECHEC"
            if status == "ECHEC":
                all_ok = False
            print(f"  {status} - {table} : {count} lignes (attendu >= {min_rows})")
        except Exception as e:
            all_ok = False
            print(f"  ECHEC - {table} : table introuvable ({e})")
    return all_ok


def test_2_completude_chargement(engine):
    print("\n[Test 2] Complétude du chargement (staging -> DW)")
    tables = pd.read_sql(text("""
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public' AND tablename LIKE 'stg_%'
    """), engine)
    all_ok = True
    for table in tables["tablename"]:
        count = pd.read_sql(text(f"SELECT COUNT(*) AS n FROM {table}"), engine)["n"][0]
        status = "OK" if count > 0 else "ECHEC"
        if status == "ECHEC":
            all_ok = False
        print(f"  {status} - {table} : {count} lignes chargées")
    return all_ok


def test_3_perte_de_donnees(engine):
    print("\n[Test 3] Perte de données lors du peuplement des faits")
    checks = [
        ("stg_postgres_paiements", "fait_paiements"),
        ("stg_mysql_notes", "fait_notes"),
    ]
    all_ok = True
    for source, fait in checks:
        n_source = pd.read_sql(text(f"SELECT COUNT(*) AS n FROM {source}"), engine)["n"][0]
        n_fait = pd.read_sql(text(f"SELECT COUNT(*) AS n FROM {fait}"), engine)["n"][0]
        taux_perte = round(100 * (1 - n_fait / n_source), 1) if n_source else 0
        status = "OK" if taux_perte < 5 else "AVERTISSEMENT"
        if status == "AVERTISSEMENT":
            all_ok = False
        print(f"  {status} - {source} ({n_source}) -> {fait} ({n_fait}) : {taux_perte}% de perte")
    return all_ok


def test_4_erreurs_execution(engine):
    print("\n[Test 4] Erreurs d'exécution (journal etl_execution_log)")
    try:
        errors = pd.read_sql(text("""
            SELECT source, date_execution, erreurs
            FROM etl_execution_log
            WHERE statut = 'echec'
            ORDER BY date_execution DESC
            LIMIT 10
        """), engine)
        if errors.empty:
            print("  OK - aucune erreur enregistrée dans l'historique")
            return True
        else:
            print(f"  ECHEC - {len(errors)} erreur(s) trouvée(s) :")
            for _, row in errors.iterrows():
                print(f"    - {row['source']} ({row['date_execution']}) : {row['erreurs']}")
            return False
    except Exception as e:
        print(f"  ECHEC - table etl_execution_log introuvable ({e})")
        return False


def test_5_validite_cles(engine):
    print("\n[Test 5] Validité des clés étrangères")
    all_ok = True
    for fait_table, fk_col, dim_table, dim_col in FK_CHECKS:
        orphans = pd.read_sql(text(f"""
            SELECT COUNT(*) AS n
            FROM {fait_table} f
            LEFT JOIN {dim_table} d ON f.{fk_col} = d.{dim_col}
            WHERE d.{dim_col} IS NULL
        """), engine)["n"][0]
        status = "OK" if orphans == 0 else "ECHEC"
        if status == "ECHEC":
            all_ok = False
        print(f"  {status} - {fait_table}.{fk_col} -> {dim_table}.{dim_col} : {orphans} clé(s) orpheline(s)")
    return all_ok


def run_all_tests():
    engine = get_engine()
    print("=" * 60)
    print("VALIDATION DU PIPELINE ETL EDUSMART")
    print("=" * 60)

    results = {
        "Complétude extraction": test_1_completude_extraction(engine),
        "Complétude chargement": test_2_completude_chargement(engine),
        "Absence de perte de données": test_3_perte_de_donnees(engine),
        "Absence d'erreurs": test_4_erreurs_execution(engine),
        "Validité des clés": test_5_validite_cles(engine),
    }

    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    for name, passed in results.items():
        print(f"  {'✓' if passed else '✗'} {name}")

    total_passed = sum(results.values())
    print(f"\n{total_passed}/{len(results)} tests réussis")

    return results


if __name__ == "__main__":
    run_all_tests()