"""
EduSmart - Source 1 : PostgreSQL - Gestion Académique
Insertion des données générées (data/*.csv) dans la base edusmart_academic.

Remarque : les enregistrements orphelins volontaires (paiements pointant
vers un etudiant_id/inscription_id inexistant) sont insérés en désactivant
temporairement la vérification des contraintes FK (session_replication_role),
afin de reproduire fidèlement une source réelle imparfaite. Les contraintes
restent déclarées dans le schéma pour la documentation et les futurs
contrôles de qualité.
"""

import csv
import os
import psycopg2

DB_CONFIG = dict(
    host="127.0.0.1",
    port=5432,
    dbname="edusmart_academic",
    user="postgres",
    password="postgres",
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_csv(filename):
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def none_if_empty(v):
    return None if v is None or v == "" else v


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    # Désactive temporairement la vérification des contraintes (pour les
    # anomalies volontaires : doublons, orphelins) puis la réactive.
    cur.execute("SET session_replication_role = 'replica';")

    filieres = load_csv("filieres.csv")
    cur.executemany(
        """INSERT INTO filieres (filiere_id, code_filiere, nom_filiere, niveau,
           duree_annees, responsable, date_creation)
           VALUES (%(filiere_id)s, %(code_filiere)s, %(nom_filiere)s, %(niveau)s,
           %(duree_annees)s, %(responsable)s, %(date_creation)s)""",
        filieres,
    )
    print(f"filieres insérées : {len(filieres)}")

    classes = load_csv("classes.csv")
    cur.executemany(
        """INSERT INTO classes (classe_id, filiere_id, nom_classe, annee_scolaire,
           effectif_max, salle)
           VALUES (%(classe_id)s, %(filiere_id)s, %(nom_classe)s, %(annee_scolaire)s,
           %(effectif_max)s, %(salle)s)""",
        classes,
    )
    print(f"classes insérées : {len(classes)}")

    etudiants = load_csv("etudiants.csv")
    for e in etudiants:
        e["email"] = none_if_empty(e["email"])
        e["telephone"] = none_if_empty(e["telephone"])
        e["ville"] = none_if_empty(e["ville"])
    cur.executemany(
        """INSERT INTO etudiants (etudiant_id, matricule, nom, prenom, date_naissance,
           sexe, email, telephone, ville, date_inscription, classe_id)
           VALUES (%(etudiant_id)s, %(matricule)s, %(nom)s, %(prenom)s, %(date_naissance)s,
           %(sexe)s, %(email)s, %(telephone)s, %(ville)s, %(date_inscription)s, %(classe_id)s)""",
        etudiants,
    )
    print(f"etudiants insérés : {len(etudiants)}")

    inscriptions = load_csv("inscriptions.csv")
    cur.executemany(
        """INSERT INTO inscriptions (inscription_id, etudiant_id, filiere_id, classe_id,
           annee_scolaire, date_inscription, statut)
           VALUES (%(inscription_id)s, %(etudiant_id)s, %(filiere_id)s, %(classe_id)s,
           %(annee_scolaire)s, %(date_inscription)s, %(statut)s)""",
        inscriptions,
    )
    print(f"inscriptions insérées : {len(inscriptions)}")

    paiements = load_csv("paiements.csv")
    cur.executemany(
        """INSERT INTO paiements (paiement_id, etudiant_id, inscription_id, montant,
           devise, mode_paiement, date_paiement, statut_paiement)
           VALUES (%(paiement_id)s, %(etudiant_id)s, %(inscription_id)s, %(montant)s,
           %(devise)s, %(mode_paiement)s, %(date_paiement)s, %(statut_paiement)s)""",
        paiements,
    )
    print(f"paiements insérés : {len(paiements)}")

    cur.execute("SET session_replication_role = 'origin';")
    conn.commit()
    cur.close()
    conn.close()
    print("Insertion terminée avec succès.")


if __name__ == "__main__":
    main()
