-- ============================================================
-- Schéma multidimensionnel EduSmart Data Warehouse
-- Star Schema / Fact Constellation
-- ============================================================

-- ==================== DIMENSIONS ====================

CREATE TABLE IF NOT EXISTS dim_temps (
    temps_id SERIAL PRIMARY KEY,
    date_complete DATE UNIQUE NOT NULL,
    jour INTEGER NOT NULL,
    mois INTEGER NOT NULL,
    nom_mois VARCHAR(20) NOT NULL,
    trimestre INTEGER NOT NULL,
    annee INTEGER NOT NULL,
    jour_semaine VARCHAR(15) NOT NULL
);
CREATE TABLE IF NOT EXISTS dim_etudiant (
    etudiant_key SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL,
    matricule VARCHAR(50),
    nom VARCHAR(100),
    prenom VARCHAR(100),
    sexe VARCHAR(10),
    ville VARCHAR(100),
    date_naissance DATE,
    date_inscription DATE,
    date_debut DATE NOT NULL DEFAULT CURRENT_DATE,
    date_fin DATE,
    est_actuel BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_dim_etudiant_actuel ON dim_etudiant(etudiant_id, est_actuel);

CREATE TABLE IF NOT EXISTS dim_formation (
    formation_key SERIAL PRIMARY KEY,
    classe_id INTEGER,
    filiere VARCHAR(150),
    classe VARCHAR(100),
    cours VARCHAR(150),
    module VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS dim_enseignant (
    enseignant_key SERIAL PRIMARY KEY,
    enseignant_id VARCHAR(50),
    nom VARCHAR(100),
    prenom VARCHAR(100),
    diplome VARCHAR(100),
    type_contrat VARCHAR(50),
    departement_id VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_region (
    region_key SERIAL PRIMARY KEY,
    ville VARCHAR(100) UNIQUE,
    departement VARCHAR(100)
);

-- ==================== FAITS ====================

CREATE TABLE IF NOT EXISTS fait_paiements (
    fait_id SERIAL PRIMARY KEY,
    temps_id INTEGER REFERENCES dim_temps(temps_id),
    etudiant_key INTEGER REFERENCES dim_etudiant(etudiant_key),
    montant NUMERIC(10, 2),
    mode_paiement VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS fait_notes (
    fait_id SERIAL PRIMARY KEY,
    temps_id INTEGER REFERENCES dim_temps(temps_id),
    etudiant_key INTEGER REFERENCES dim_etudiant(etudiant_key),
    formation_key INTEGER REFERENCES dim_formation(formation_key),
    note NUMERIC(4, 2)
);

CREATE TABLE IF NOT EXISTS fait_connexions (
    fait_id SERIAL PRIMARY KEY,
    temps_id INTEGER REFERENCES dim_temps(temps_id),
    etudiant_key INTEGER REFERENCES dim_etudiant(etudiant_key),
    duree_minutes NUMERIC(10, 2),
    nombre_connexions INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS fait_quiz (
    fait_id SERIAL PRIMARY KEY,
    temps_id INTEGER REFERENCES dim_temps(temps_id),
    etudiant_key INTEGER REFERENCES dim_etudiant(etudiant_key),
    formation_key INTEGER REFERENCES dim_formation(formation_key),
    score NUMERIC(5, 2)
);

-- ==================== INDEX ====================

CREATE INDEX IF NOT EXISTS idx_fait_paiements_temps ON fait_paiements(temps_id);
CREATE INDEX IF NOT EXISTS idx_fait_paiements_etudiant ON fait_paiements(etudiant_key);
CREATE INDEX IF NOT EXISTS idx_fait_notes_temps ON fait_notes(temps_id);
CREATE INDEX IF NOT EXISTS idx_fait_notes_etudiant ON fait_notes(etudiant_key);
CREATE INDEX IF NOT EXISTS idx_fait_connexions_temps ON fait_connexions(temps_id);
CREATE INDEX IF NOT EXISTS idx_fait_connexions_etudiant ON fait_connexions(etudiant_key);
CREATE INDEX IF NOT EXISTS idx_fait_quiz_temps ON fait_quiz(temps_id);
CREATE INDEX IF NOT EXISTS idx_fait_quiz_etudiant ON fait_quiz(etudiant_key);