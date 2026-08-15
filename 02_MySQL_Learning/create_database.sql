-- =====================================================================
-- EduSmart - Source 2 : MySQL - Plateforme pédagogique
-- Base : edusmart_learning
-- =====================================================================
-- Modules, Cours, Quiz, Notes, Progression, Temps de connexion.
-- Les identifiants d'étudiant (etudiant_id) référencent en toute logique
-- les étudiants de la base PostgreSQL (edusmart_academic), mais AUCUNE
-- contrainte FK physique n'est possible entre deux SGBD différents :
-- c'est précisément ce que devra gérer la phase d'intégration ETL.
-- =====================================================================

DROP TABLE IF EXISTS temps_connexion;
DROP TABLE IF EXISTS progression;
DROP TABLE IF EXISTS notes;
DROP TABLE IF EXISTS quiz;
DROP TABLE IF EXISTS cours;
DROP TABLE IF EXISTS modules;

-- ---------------------------------------------------------------------
CREATE TABLE modules (
    module_id       INT AUTO_INCREMENT PRIMARY KEY,
    code_module     VARCHAR(20) NOT NULL,
    titre           VARCHAR(150) NOT NULL,
    filiere_code    VARCHAR(20),          -- lien logique vers filieres (PostgreSQL)
    semestre        VARCHAR(10),
    credits         SMALLINT
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
CREATE TABLE cours (
    cours_id        INT AUTO_INCREMENT PRIMARY KEY,
    module_id       INT,
    titre_cours     VARCHAR(150),
    type_cours      VARCHAR(30),          -- video, pdf, live, article
    duree_minutes   INT,
    date_publication DATE,
    FOREIGN KEY (module_id) REFERENCES modules(module_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
CREATE TABLE quiz (
    quiz_id         INT AUTO_INCREMENT PRIMARY KEY,
    cours_id        INT,
    titre_quiz      VARCHAR(150),
    nb_questions    INT,
    note_max        DECIMAL(5,2) DEFAULT 20.00,
    FOREIGN KEY (cours_id) REFERENCES cours(cours_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Table notes : pas de FK vers etudiant_id (base externe / autre SGBD)
-- ---------------------------------------------------------------------
CREATE TABLE notes (
    note_id         INT AUTO_INCREMENT PRIMARY KEY,
    etudiant_id     INT NOT NULL,          -- réfère edusmart_academic.etudiants (autre SGBD)
    quiz_id         INT,
    note_obtenue    DECIMAL(6,2),
    date_passage    DATETIME,
    tentative       SMALLINT DEFAULT 1,
    FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
CREATE TABLE progression (
    progression_id  INT AUTO_INCREMENT PRIMARY KEY,
    etudiant_id     INT NOT NULL,
    cours_id        INT,
    pourcentage_completion DECIMAL(5,2),   -- 0 à 100
    statut          VARCHAR(30),           -- non_commence, en_cours, termine
    derniere_activite DATETIME,
    FOREIGN KEY (cours_id) REFERENCES cours(cours_id)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
CREATE TABLE temps_connexion (
    session_id      INT AUTO_INCREMENT PRIMARY KEY,
    etudiant_id     INT NOT NULL,
    date_connexion  DATE,
    heure_debut     TIME,
    duree_minutes   INT,
    appareil        VARCHAR(30)            -- Android, iOS, Web, Desktop
) ENGINE=InnoDB;

CREATE INDEX idx_notes_etudiant ON notes(etudiant_id);
CREATE INDEX idx_progression_etudiant ON progression(etudiant_id);
CREATE INDEX idx_connexion_etudiant ON temps_connexion(etudiant_id);
