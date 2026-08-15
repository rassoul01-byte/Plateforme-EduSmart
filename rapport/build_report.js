const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
  TableCell, WidthType, ShadingType, AlignmentType, BorderStyle, PageBreak,
  LevelFormat, convertInchesToTwip,
} = require("docx");
const fs = require("fs");

const COLOR_PRIMARY = "1F4E5F";
const COLOR_ACCENT = "2E86AB";

function h1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 400, after: 200 } });
}
function h2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 300, after: 150 } });
}
function h3(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_3, spacing: { before: 200, after: 100 } });
}
function p(text, opts = {}) {
  return new Paragraph({ children: [new TextRun({ text, ...opts })], spacing: { after: 120 } });
}
function bullet(text) {
  return new Paragraph({ text, bullet: { level: 0 }, spacing: { after: 60 } });
}

function cell(text, { header = false, width } = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: header ? { type: ShadingType.CLEAR, color: "auto", fill: "1F4E5F" } : undefined,
    children: [new Paragraph({
      children: [new TextRun({ text: String(text), bold: header, color: header ? "FFFFFF" : "000000", size: 20 })],
    })],
  });
}

function simpleTable(headers, rows, widths) {
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ children: headers.map((h, i) => cell(h, { header: true, width: widths[i] })) }),
      ...rows.map((r) => new TableRow({ children: r.map((v, i) => cell(v, { width: widths[i] })) })),
    ],
  });
}

function sourceSection(num, titre, techno, structureRows, structureWidths, relations, contraintes, anomalies, volumes) {
  return [
    h1(`Source ${num} — ${titre}`),
    p(`Technologie : ${techno}`, { italics: true, color: COLOR_ACCENT }),
    h2("1. Structure de la source"),
    simpleTable(["Table / Fichier / Clé", "Description"], structureRows, structureWidths),
    h2("2. Relations internes"),
    ...relations.map(bullet),
    h2("3. Contraintes mises en place"),
    ...contraintes.map(bullet),
    h2("4. Anomalies introduites volontairement"),
    ...anomalies.map(bullet),
    h2("5. Volume de données généré"),
    simpleTable(["Élément", "Volume"], volumes, [5000, 3000]),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

const doc = new Document({
  sections: [
    {
      properties: { page: { size: { width: 11906, height: 16838 } } }, // A4
      children: [
        new Paragraph({ text: "", spacing: { before: 2000 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "EduSmart", bold: true, size: 64, color: COLOR_PRIMARY })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 200 },
          children: [new TextRun({ text: "Plateforme décisionnelle — Mise en place des 5 sources de données", size: 28, color: COLOR_ACCENT })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 600 },
          children: [new TextRun({ text: "Document de présentation", size: 24 })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 3000 },
          children: [new TextRun({ text: "Projet réalisé intégralement en solo — 5 sources : PostgreSQL, MySQL, CSV, JSON, Redis", size: 20, italics: true })],
        }),
        new Paragraph({ children: [new PageBreak()] }),

        h1("Contexte du projet"),
        p("EduSmart est une plateforme de formation en ligne. Au fil des années, plusieurs applications ont été développées, chacune avec sa propre base de données. L'objectif est de construire une plateforme décisionnelle unique permettant d'analyser l'ensemble des activités de l'entreprise."),
        p("Ce document couvre la première étape du projet : la mise en place complète des cinq sources de données hétérogènes qui seront ensuite extraites, nettoyées, transformées et intégrées dans un entrepôt de données décisionnel unique."),
        h2("Vue d'ensemble des 5 sources"),
        simpleTable(
          ["Source", "Technologie", "Domaine métier"],
          [
            ["1", "PostgreSQL", "Gestion académique (étudiants, filières, classes, inscriptions, paiements)"],
            ["2", "MySQL", "Plateforme pédagogique (modules, cours, quiz, notes, progression, connexions)"],
            ["3", "CSV", "Ressources humaines (enseignants, salaires, départements, absences)"],
            ["4", "JSON", "Journaux de l'application mobile (événements utilisateurs)"],
            ["5", "Redis", "Plateforme temps réel (sessions, progression live, notifications)"],
          ],
          [1000, 2500, 5500]
        ),
        new Paragraph({ children: [new PageBreak()] }),

        ...sourceSection(
          1, "PostgreSQL — Gestion Académique", "PostgreSQL 16 — base edusmart_academic",
          [
            ["filieres", "Référentiel des filières de formation (code, niveau, durée, responsable)"],
            ["classes", "Classes rattachées à une filière (année scolaire, effectif, salle)"],
            ["etudiants", "Fiche étudiant (identité, contact, ville, classe)"],
            ["inscriptions", "Historique des inscriptions d'un étudiant à une filière/classe"],
            ["paiements", "Paiements liés à une inscription (montant, mode, statut)"],
          ],
          [2200, 6800],
          [
            "filieres (1,n) classes : une filière comporte plusieurs classes",
            "classes (1,n) etudiants : une classe regroupe plusieurs étudiants",
            "etudiants (1,n) inscriptions : un étudiant peut avoir plusieurs inscriptions (réinscriptions)",
            "inscriptions (1,n) paiements : plusieurs paiements peuvent être liés à une inscription",
          ],
          [
            "Clés primaires SERIAL sur toutes les tables",
            "Clés étrangères : classes.filiere_id, etudiants.classe_id, inscriptions.etudiant_id/filiere_id/classe_id, paiements.etudiant_id/inscription_id",
            "Index sur les colonnes de jointure fréquentes (etudiant_id, classe_id)",
            "Le champ matricule n'est volontairement PAS contraint en UNIQUE (anomalie réaliste à traiter en ETL)",
          ],
          [
            "889 e-mails manquants (valeurs vides)",
            "150 étudiants dupliqués (même matricule ré-inséré)",
            "Champ sexe mal standardisé : \"M\", \"F\", \"Homme\", \"Femme\", \"H\", \"m\", \"f\", vide",
            "617 paiements orphelins (etudiant_id / inscription_id inexistants)",
            "578 paiements à montant négatif (erreur de saisie)",
            "Formats de téléphone hétérogènes (+221XXXXXXXXX, XX-XX-XX-XX, brut)",
            "~3% de dates de naissance postérieures à la date d'inscription (incohérence)",
            "Un format d'identifiant \"matricule\" legacy incompatible (numérique brut) coexiste avec le format standard ETUxxxxNNNN",
          ],
          [
            ["Filières", "15"], ["Classes", "220"], ["Étudiants", "15 150 (dont 150 doublons volontaires)"],
            ["Inscriptions", "18 000"], ["Paiements", "30 000"],
          ]
        ),

        ...sourceSection(
          2, "MySQL — Plateforme Pédagogique", "MySQL 8.0 — base edusmart_learning",
          [
            ["modules", "Modules de formation (crédits, semestre, filière liée par code)"],
            ["cours", "Contenus pédagogiques rattachés à un module (type, durée)"],
            ["quiz", "Évaluations rattachées à un cours"],
            ["notes", "Résultats des étudiants aux quiz (etudiant_id externe, non-FK)"],
            ["progression", "Pourcentage d'avancement d'un étudiant sur un cours"],
            ["temps_connexion", "Sessions de connexion (durée, appareil utilisé)"],
          ],
          [2200, 6800],
          [
            "modules (1,n) cours : un module regroupe plusieurs cours",
            "cours (1,n) quiz : un cours peut avoir plusieurs quiz",
            "quiz (1,n) notes : un quiz reçoit plusieurs notes d'étudiants",
            "etudiant_id (notes, progression, temps_connexion) référence logiquement la base PostgreSQL — pas de FK physique inter-SGBD, à réconcilier lors de l'intégration",
          ],
          [
            "Clés primaires AUTO_INCREMENT sur toutes les tables",
            "Clés étrangères internes : cours.module_id, quiz.cours_id, notes.quiz_id, progression.cours_id",
            "Moteur InnoDB (transactionnel) avec index sur les colonnes etudiant_id",
            "Aucune contrainte FK n'est possible vers la table etudiants (autre SGBD) : anomalie structurelle inhérente à l'architecture multi-source",
          ],
          [
            "350 doublons stricts dans la table notes (retransmission applicative)",
            "1 335 notes hors barème (supérieures à 20, erreur de saisie)",
            "879 notes manquantes (champ vide)",
            "Casse incohérente sur type_cours (video/Video/PDF) et statut (en_cours/EN_COURS)",
            "1 065 pourcentages de progression hors bornes (>100%)",
            "1 039 durées de connexion aberrantes (négatives ou 999 minutes)",
            "Champ appareil parfois vide ou en casse variable (Android/android/IOS)",
          ],
          [
            ["Modules", "20"], ["Cours", "120"], ["Quiz", "150"],
            ["Notes", "45 350"], ["Progression", "55 000"], ["Temps de connexion", "70 000"],
          ]
        ),

        ...sourceSection(
          3, "CSV — Ressources Humaines", "4 fichiers CSV indépendants (exports RH)",
          [
            ["departements.csv", "Référentiel des départements (id, nom, responsable, budget)"],
            ["enseignants.csv", "Fiche enseignant (identité, département, diplôme, contrat)"],
            ["salaires.csv", "Historique mensuel de paie par enseignant"],
            ["absences.csv", "Déclarations d'absence par enseignant"],
          ],
          [2200, 6800],
          [
            "departements (1,n) enseignants via departement_id",
            "enseignants (1,n) salaires et enseignants (1,n) absences via enseignant_id",
            "Les 4 fichiers sont totalement indépendants (pas d'intégrité référentielle native, contrairement à une base relationnelle)",
          ],
          [
            "Aucune contrainte technique (le format CSV ne permet ni PK ni FK)",
            "Cohérence assurée uniquement par convention de nommage des identifiants au moment de la génération",
            "Description de structure fournie dans ce document en lieu et place d'un schéma SQL",
          ],
          [
            "Formats d'identifiant enseignant hétérogènes : ENS0001 (standard), 1001 (numérique brut), ens_12 (legacy) — incompatibles entre eux",
            "18 doublons stricts dans enseignants.csv",
            "36 e-mails manquants",
            "Dates d'embauche sur deux formats différents (AAAA-MM-JJ vs JJ/MM/AAAA)",
            "type_contrat mal standardisé (CDI/cdi, espaces parasites)",
            "138 lignes salaires.csv référencent un enseignant_id absent de enseignants.csv (identifiant OLDxxx, migration incomplète)",
            "74 salaires manquants (champ vide)",
            "39 absences avec enseignant_id inconnu (orphelins)",
            "~2% d'absences avec date_fin antérieure à date_debut (incohérence)",
            "Champ justifiee incohérent (Oui/oui/Non/non/vide)",
          ],
          [
            ["Départements", "8"], ["Enseignants", "468"],
            ["Salaires (lignes de paie)", "3 500"], ["Absences", "1 400"],
          ]
        ),

        ...sourceSection(
          4, "JSON — Journaux Application Mobile", "Fichiers JSON / JSON Lines (logs d'événements)",
          [
            ["event_id", "Identifiant unique de l'événement"],
            ["student_id", "Référence logique vers etudiants (PostgreSQL), parfois null"],
            ["event", "Type d'action (App Opened, Quiz Started, Login, ...)"],
            ["device", "Appareil utilisé (Android/iOS/Web), champ parfois absent"],
            ["city", "Ville de connexion, parfois null"],
            ["timestamp", "Horodatage de l'événement (format non garanti)"],
          ],
          [2200, 6800],
          [
            "student_id référence logiquement etudiants.etudiant_id de la source PostgreSQL",
            "Schéma non strict (schemaless) : certains événements portent un champ additionnel app_version absent des autres",
          ],
          [
            "Aucune contrainte native (JSON schemaless) — un script create_source.py documente et valide la structure logique attendue",
            "event_id conçu comme identifiant fonctionnel unique (non garanti par le format lui-même)",
          ],
          [
            "2 227 student_id manquants (null) — événements mal tracés",
            "Valeurs event incohérentes en casse/format (Quiz Started vs quiz_started vs QUIZ_COMPLETED)",
            "19 201 événements avec device manquant, vide ou en casse variable (Android/android/IOS)",
            "~5% de timestamps au format JJ/MM/AAAA HH:MM:SS au lieu d'ISO-8601",
            "~1% de doublons exacts (retransmission réseau côté mobile)",
            "280 événements avec le champ device totalement absent (clé manquante)",
            "Ville parfois null ou chaîne vide",
          ],
          [["Événements générés", "113 435"], ["Anomalies structurelles détectées", "21 068"]]
        ),

        ...sourceSection(
          5, "Redis — Plateforme Temps Réel", "Redis 7 — base logique db=1 dédiée EduSmart",
          [
            ["session:{student_id}", "HASH — statut de connexion courant (status, last_course, last_activity)"],
            ["active_sessions", "SET — ensemble des étudiants actuellement en ligne"],
            ["progress:{student_id}:{course_id}", "STRING — pourcentage de progression en temps réel"],
            ["last_quiz:{student_id}", "HASH — dernier quiz réalisé (quiz_id, score, timestamp)"],
            ["notifications:{student_id}", "LIST — file de notifications en attente"],
          ],
          [3200, 5800],
          [
            "student_id (dans toutes les clés) référence logiquement etudiants.etudiant_id (PostgreSQL)",
            "course_id / quiz_id référencent logiquement cours/quiz (MySQL)",
            "active_sessions est dérivé de l'ensemble des session:{id} au statut \"online\"",
          ],
          [
            "TTL (expire) posé sur chaque clé session et progress pour simuler le caractère éphémère du temps réel",
            "Une base logique dédiée (db=1) isole les données EduSmart du reste de l'instance Redis",
            "Pas de contrainte relationnelle possible (moteur clé-valeur) : la cohérence est uniquement applicative",
          ],
          [
            "Champ status non standardisé (online/ONLINE/en_ligne/offline/idle/vide)",
            "169 sessions sans le champ last_course (clé manquante dans le hash)",
            "~4% de last_activity dans un format de date différent (JJ/MM/AAAA HH:MM)",
            "128 pourcentages de progression hors bornes (>100%)",
            "73 notifications référencent un student_id hors plage connue (orphelin, >15150)",
            "Certains étudiants n'ont aucune notification en attente (liste vide), simulant l'hétérogénéité réelle des usages",
          ],
          [
            ["Sessions actives simulées", "5 600"], ["Sessions réellement \"online\"", "2 625"],
            ["Progressions temps réel", "7 500"], ["Derniers quiz", "3 500"],
            ["Étudiants avec notifications", "2 800"], ["Clés Redis totales (db=1)", "17 812"],
          ]
        ),

        h1("Synthèse et prochaines étapes"),
        p("Les cinq sources de données ont été intégralement mises en place, chacune avec sa structure documentée, un script de génération de données réalistes (Faker) et un volume cohérent avec le contexte métier d'EduSmart."),
        p("Conformément à la consigne, chaque source contient des anomalies volontaires représentatives d'un environnement réel : valeurs manquantes, doublons, formats hétérogènes, catégories mal standardisées, dates incohérentes, identifiants incompatibles entre sources et enregistrements orphelins."),
        h2("Tableau récapitulatif des volumes"),
        simpleTable(
          ["Source", "Nombre total d'enregistrements"],
          [
            ["PostgreSQL (5 tables)", "63 385"],
            ["MySQL (6 tables)", "170 640"],
            ["CSV (4 fichiers)", "5 376"],
            ["JSON (logs mobile)", "113 435"],
            ["Redis (5 structures de clés)", "17 812 clés"],
          ],
          [5000, 4000]
        ),
        p(""),
        p("Ces sources constituent désormais la base de départ pour la phase suivante du projet : extraction, nettoyage/transformation des anomalies, conservation des métadonnées, et intégration dans une base décisionnelle unique alimentant les tableaux de bord EduSmart.", { italics: true }),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(__dirname + "/Rapport_EduSmart.docx", buf);
  console.log("Rapport généré.");
});
