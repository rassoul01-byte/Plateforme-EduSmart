# Plateforme EduSmart — Pipeline ELK

Projet TP réalisé dans le cadre du programme **DEV DATA P8** (Sonatel Academy / Orange Digital Center, Dakar).

## Objectif

EduSmart est une plateforme de formation en ligne fictive dont les données sont réparties sur plusieurs systèmes hétérogènes. Ce projet consiste à **ingérer, unifier et visualiser** ces données à l'aide de la stack **ELK (Elasticsearch, Logstash, Kibana)** conteneurisée avec **Docker**.

## Sources de données

| # | Source | Technologie | Contenu | Volume |
|---|--------|-------------|---------|--------|
| 1 | Académique | PostgreSQL | Étudiants, classes, inscriptions, paiements | ~15 150 étudiants, 18 000 inscriptions, 30 000 paiements |
| 2 | Learning (LMS) | MySQL | Modules, cours, quiz, notes, progression, temps de connexion | ~45 350 notes, 55 000 lignes de progression |
| 3 | Ressources Humaines | CSV | Départements, enseignants, salaires, absences | 468 enseignants, 3 500 salaires |
| 4 | Logs mobile | JSON / JSONL | Événements d'usage de l'application mobile | 113 435 événements (dont anomalies structurelles) |
| 5 | Temps réel | Redis | Sessions actives, progression en direct, quiz, notifications | 5 600 sessions, 2 625 actives |

## Architectures











Chaque dossier de source contient :
- `create_database.sql` ou `create_source.py` : création du schéma / initialisation
- `generate_data.py` : génération de données synthétiques (via Faker)
- `insert_data.py` : insertion des données dans le système cible

## Mise en route

### 1. Démarrer les services de base de données

```bash
service postgresql start
service mysql start
service redis-server start
```

### 2. Installer les dépendances Python

```bash
pip install --break-system-packages faker mysql-connector-python psycopg2-binary redis
```

### 3. Générer et insérer les données (par source)

**PostgreSQL**
```bash
cd 01_PostgreSQL_Academique
PGPASSWORD=postgres psql -h 127.0.0.1 -U postgres -d postgres -c "CREATE DATABASE edusmart_academic;"
PGPASSWORD=postgres psql -h 127.0.0.1 -U postgres -d edusmart_academic -f create_database.sql
python3 generate_data.py
python3 insert_data.py
```

**MySQL**
```bash
cd 02_MySQL_Learning
mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS edusmart_learning;"
mysql -u root -proot edusmart_learning < create_database.sql
python3 generate_data.py
python3 insert_data.py
```

**CSV (RH)**
```bash
cd 03_CSV_RH
python3 generate_data.py
```

**JSON (logs mobile)**
```bash
cd 04_JSON_Logs
python3 generate_data.py
python3 create_source.py
```

**Redis (temps réel)**
```bash
cd 05_Redis_TempsReel
python3 create_source.py
python3 generate_data.py
python3 insert_data.py
```

## Prochaine étape : pipeline Docker / ELK

- [ ] Configuration `docker-compose.yml` (Elasticsearch, Logstash, Kibana)
- [ ] Pipelines Logstash par source (JDBC input pour PostgreSQL/MySQL, file input pour CSV/JSON, Redis input)
- [ ] Indexation dans Elasticsearch
- [ ] Dashboards Kibana

## Auteur

Seydina Wade — Étudiant DEV DATA P8, Sonatel Academy / Orange Digital Center (Dakar) & UCAD (Licence MPI)

## Licence

Projet académique — usage pédagogique.