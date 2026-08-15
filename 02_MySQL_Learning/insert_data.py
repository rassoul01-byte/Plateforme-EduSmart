"""
EduSmart - Source 2 : MySQL - Plateforme pédagogique
Insertion des données générées (data/*.csv) dans la base edusmart_learning.
"""

import csv
import os
import mysql.connector

DB_CONFIG = dict(
    host="127.0.0.1",
    user="root",
    password="root",
    database="edusmart_learning",
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_csv(filename):
    with open(os.path.join(DATA_DIR, filename), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def none_if_empty(v):
    return None if v is None or v == "" else v


def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0;")

    modules = load_csv("modules.csv")
    cur.executemany(
        "INSERT INTO modules (module_id, code_module, titre, filiere_code, semestre, credits) "
        "VALUES (%(module_id)s, %(code_module)s, %(titre)s, %(filiere_code)s, %(semestre)s, %(credits)s)",
        modules,
    )
    print(f"modules insérés : {len(modules)}")

    cours = load_csv("cours.csv")
    cur.executemany(
        "INSERT INTO cours (cours_id, module_id, titre_cours, type_cours, duree_minutes, date_publication) "
        "VALUES (%(cours_id)s, %(module_id)s, %(titre_cours)s, %(type_cours)s, %(duree_minutes)s, %(date_publication)s)",
        cours,
    )
    print(f"cours insérés : {len(cours)}")

    quiz = load_csv("quiz.csv")
    cur.executemany(
        "INSERT INTO quiz (quiz_id, cours_id, titre_quiz, nb_questions, note_max) "
        "VALUES (%(quiz_id)s, %(cours_id)s, %(titre_quiz)s, %(nb_questions)s, %(note_max)s)",
        quiz,
    )
    print(f"quiz insérés : {len(quiz)}")

    notes = load_csv("notes.csv")
    for n in notes:
        n["note_obtenue"] = none_if_empty(n["note_obtenue"])
    cur.executemany(
        "INSERT INTO notes (note_id, etudiant_id, quiz_id, note_obtenue, date_passage, tentative) "
        "VALUES (%(note_id)s, %(etudiant_id)s, %(quiz_id)s, %(note_obtenue)s, %(date_passage)s, %(tentative)s)",
        notes,
    )
    print(f"notes insérées : {len(notes)}")

    progression = load_csv("progression.csv")
    cur.executemany(
        "INSERT INTO progression (progression_id, etudiant_id, cours_id, pourcentage_completion, statut, derniere_activite) "
        "VALUES (%(progression_id)s, %(etudiant_id)s, %(cours_id)s, %(pourcentage_completion)s, %(statut)s, %(derniere_activite)s)",
        progression,
    )
    print(f"progression insérée : {len(progression)}")

    temps_connexion = load_csv("temps_connexion.csv")
    cur.executemany(
        "INSERT INTO temps_connexion (session_id, etudiant_id, date_connexion, heure_debut, duree_minutes, appareil) "
        "VALUES (%(session_id)s, %(etudiant_id)s, %(date_connexion)s, %(heure_debut)s, %(duree_minutes)s, %(appareil)s)",
        temps_connexion,
    )
    print(f"temps_connexion insérés : {len(temps_connexion)}")

    cur.execute("SET FOREIGN_KEY_CHECKS=1;")
    conn.commit()
    cur.close()
    conn.close()
    print("Insertion terminée avec succès.")


if __name__ == "__main__":
    main()
