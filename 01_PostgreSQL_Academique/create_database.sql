-- =====================================================================
-- EduSmart - Source 1 : PostgreSQL - Gestion Académique
-- Base : edusmart_academic
-- =====================================================================
-- Ce script crée la structure complète de la base académique :
-- Filières, Classes, Étudiants, Inscriptions, Paiements.
-- Des contraintes (clés primaires, clés étrangères, CHECK, UNIQUE) sont
-- posées là où la logique métier l'exige. Certaines colonnes restent
-- volontairement peu contraintes (ex : email, téléphone) pour permettre
-- l'injection d'anomalies réalistes lors de la génération des données.
-- =====================================================================

DROP TABLE IF EXISTS paiements CASCADE;
DROP TABLE IF EXISTS inscriptions CASCADE;
DROP TABLE IF EXISTS etudiants CASCADE;
DROP TABLE IF EXISTS classes CASCADE;
DROP TABLE IF EXISTS filieres CASCADE;

-- ---------------------------------------------------------------------
-- Table : filieres
-- ---------------------------------------------------------------------
CREATE TABLE filieres (
    filiere_id      SERIAL PRIMARY KEY,
    code_filiere    VARCHAR(20) UNIQUE NOT NULL,
    nom_filiere     VARCHAR(150) NOT NULL,
    niveau          VARCHAR(30),              -- Licence, Master, Bachelor...
    duree_annees    SMALLINT,
    responsable     VARCHAR(150),
    date_creation   DATE
);

-- ---------------------------------------------------------------------
-- Table : classes
-- ---------------------------------------------------------------------
CREATE TABLE classes (
    classe_id       SERIAL PRIMARY KEY,
    filiere_id      INTEGER REFERENCES filieres(filiere_id),
    nom_classe      VARCHAR(100) NOT NULL,
    annee_scolaire  VARCHAR(20),               -- ex : "2025-2026"
    effectif_max    INTEGER,
    salle           VARCHAR(50)
);

-- ---------------------------------------------------------------------
-- Table : etudiants
-- ---------------------------------------------------------------------
CREATE TABLE etudiants (
    etudiant_id     SERIAL PRIMARY KEY,
    matricule       VARCHAR(20),           -- pas de UNIQUE : des doublons de matricule existent dans la source réelle (anomalie à traiter en ETL)
    nom             VARCHAR(100),
    prenom          VARCHAR(100),
    date_naissance  DATE,
    sexe            VARCHAR(10),
    email           VARCHAR(150),               -- pas de UNIQUE -> doublons possibles (anomalie)
    telephone       VARCHAR(30),
    ville           VARCHAR(100),
    date_inscription DATE,
    classe_id       INTEGER REFERENCES classes(classe_id)
);

-- ---------------------------------------------------------------------
-- Table : inscriptions
-- ---------------------------------------------------------------------
CREATE TABLE inscriptions (
    inscription_id  SERIAL PRIMARY KEY,
    etudiant_id     INTEGER REFERENCES etudiants(etudiant_id),
    filiere_id      INTEGER REFERENCES filieres(filiere_id),
    classe_id       INTEGER REFERENCES classes(classe_id),
    annee_scolaire  VARCHAR(20),
    date_inscription DATE,
    statut          VARCHAR(30)      -- active, terminee, abandonnee...
);

-- ---------------------------------------------------------------------
-- Table : paiements
-- ---------------------------------------------------------------------
CREATE TABLE paiements (
    paiement_id     SERIAL PRIMARY KEY,
    etudiant_id     INTEGER REFERENCES etudiants(etudiant_id),
    inscription_id  INTEGER REFERENCES inscriptions(inscription_id),
    montant         NUMERIC(12,2),
    devise          VARCHAR(10) DEFAULT 'XOF',
    mode_paiement   VARCHAR(30),      -- especes, mobile money, virement, cheque
    date_paiement   TIMESTAMP,
    statut_paiement VARCHAR(30)       -- paye, en_attente, echoue, rembourse
);

-- Index utiles pour les jointures / analyses
CREATE INDEX idx_etudiants_classe ON etudiants(classe_id);
CREATE INDEX idx_inscriptions_etudiant ON inscriptions(etudiant_id);
CREATE INDEX idx_paiements_etudiant ON paiements(etudiant_id);
