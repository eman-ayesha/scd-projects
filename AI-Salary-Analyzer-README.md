# AI Salary Analyzer

A Django web application that helps users track their tech skills, estimate salary ranges for those skills, get a matched job board, and follow a personalized (or preset) career roadmap with progress tracking. Backed by MySQL, with a real Kaggle job-market dataset for the job board.

## What it actually does

- **Accounts** — custom user model (`users.CustomUser`) extending Django's `AbstractUser` with career interest, education level, and a profile photo.
- **Skill tracking** — users add skills from a shared catalog (`skills.Skill`) at a self-reported proficiency level, stored per-user in `UserSkill`.
- **Salary estimator** (`users:ai_engine`) — pick one of your saved skills and a currency; the app estimates a salary range for that skill using its base salary plus demand/growth multipliers, then converts to the selected currency (USD, EUR, GBP, PKR, INR, AED).
- **Job board** (`jobs:jobs_list`) — lists real jobs imported from `job_market_dataset.csv`. If you're logged in with saved skills, jobs are ranked by keyword overlap with your skills (`SKILL_KEYWORD_MAP`); if there aren't enough real matches, realistic placeholder listings are generated from per-skill blueprints (`SKILL_JOB_BLUEPRINTS`) to fill out the page, clearly flagged as `is_generated`.
- **Career roadmaps** (`users:roadmap`) — either follow a preset roadmap for a career goal (Data Scientist, AI Engineer, Software Engineer, DevOps Engineer) or get a personalized step-by-step roadmap generated per saved skill. Roadmaps are saved to the database and steps can be checked off, with automatic progress-percentage tracking and a completion message when every step is done.

## Honest note on the "AI" in the name

There's no trained ML model here — `ai_engine` and `analytics` are scaffolded Django apps with no models or logic yet (empty `models.py`/`views.py`). The actual "AI Engine" feature that's live lives in `users/views.py`: it's a **rule-based heuristic** — a lookup table of base salaries per skill category, adjusted by demand/growth scores, plus a keyword-matching system for job recommendations and a predefined skill-to-roadmap mapping. Worth knowing so you can describe it accurately if asked — it's a deterministic recommendation engine, not a trained model.

## Project Structure

```
config/          Django project settings, root urls, wsgi/asgi
users/            Custom user model, auth views, salary estimator, roadmap view
skills/            Skill catalog model + seed_skills management command
jobs/               Job model, job board view with skill-matching, import_data management command
roadmap/            UserRoadmap / RoadmapStep models (saved roadmap progress)
ai_engine/          Scaffolded, currently unused
analytics/           Scaffolded, currently unused
templates/           HTML templates (base, home, jobs list, users: login/register/profile/ai_engine/roadmap)
job_market_dataset.csv   Source data for the job board (Kaggle dataset)
generate_doc.py, read_docx.py   Standalone dev scripts (docx generation/reading) — not part of the running app
```

## Setup

1. **Install dependencies** (create a virtualenv first):
   ```bash
   pip install django mysqlclient python-dotenv djangorestframework
   ```
   (`rest_framework` is in `INSTALLED_APPS` but not yet used by any endpoint.)

2. **Configure the database** — copy `.env.example` to `.env` and fill in your MySQL credentials:
   ```
   MYSQL_DB=ai_salary_analyzer
   MYSQL_USER=root
   MYSQL_PASSWORD=<your password>
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   ```
   Create the database itself first: `CREATE DATABASE ai_salary_analyzer;`

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Seed the skill catalog**:
   ```bash
   python manage.py seed_skills
   ```

5. **Import the job dataset**:
   ```bash
   python manage.py import_data
   ```

6. **Create an admin user** (optional, for `/admin/`):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## Key URLs

| URL | Purpose |
|---|---|
| `/` | Home page |
| `/users/register/`, `/users/login/` | Auth |
| `/users/profile/` | Manage your skills and profile |
| `/users/ai-engine/` | Salary estimator |
| `/users/roadmap/` | Career roadmap (preset or personalized) |
| `/jobs/` | Job board, skill-matched if logged in |
| `/admin/` | Django admin |
