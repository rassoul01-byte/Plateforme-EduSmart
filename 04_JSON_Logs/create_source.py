"""
EduSmart - Source 4 : JSON - Journaux de l'application mobile
Ce fichier ne "crée" pas de base au sens SQL : une source JSON est
schemaless par nature. Il documente et valide la structure logique
attendue pour chaque événement (équivalent d'un schéma de validation),
conformément à la consigne "définir les types de données appropriés".

Champs :
  event_id      (string, obligatoire)  identifiant unique de l'événement
  student_id    (int | null)           référence logique vers etudiants (PostgreSQL)
  event         (string)               type d'action réalisée
  device        (string, optionnel)    Android / iOS / Web
  city          (string | null)        ville de connexion
  timestamp     (string ISO-8601 ou JJ/MM/AAAA HH:MM:SS - format non garanti)
  app_version   (string, optionnel)    présent uniquement sur certains événements

Ce script fournit une fonction de validation légère utilisée pour
vérifier la cohérence structurelle avant remise (voir §4 du sujet).
"""

import json
import os

REQUIRED_FIELDS = {"event_id", "student_id", "event", "city", "timestamp"}


def validate_event(evt: dict) -> list:
    """Retourne la liste des anomalies structurelles détectées (à titre indicatif,
    ces anomalies sont volontaires et seront traitées lors de l'étape ETL)."""
    issues = []
    missing = REQUIRED_FIELDS - evt.keys()
    if missing:
        issues.append(f"champs manquants: {missing}")
    if evt.get("student_id") is None:
        issues.append("student_id manquant (null)")
    if not evt.get("device"):
        issues.append("device manquant/vide")
    return issues


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "logs_mobile.json")
    if not os.path.exists(path):
        print("Aucun fichier logs_mobile.json trouvé - exécutez d'abord generate_data.py")
    else:
        with open(path, encoding="utf-8") as f:
            events = json.load(f)
        total_issues = sum(1 for e in events if validate_event(e))
        print(f"{len(events)} événements chargés, {total_issues} avec anomalies structurelles détectées.")
