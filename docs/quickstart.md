# Quickstart Guide

This guide walks you through setting up the project for local development.

## Prerequisites

- **Python 3.13+** — [Download](https://www.python.org/downloads/)
- **Docker & Docker Compose** — [Install Docker](https://docs.docker.com/get-docker/)
- **Conda** (optional) — [Install Miniconda](https://docs.conda.io/en/latest/miniconda.html)

## Option A: Docker Development (Recommended)

### 1. Clone the Repository
```bash
git clone <your-repo-url>  # TODO: Add your repo URL
cd myproject
```

### 2. Set Up Environment
```bash
make setup-env
```
This copies `.env.example` to `.env` and generates a random `SECRET_KEY`. Review the `.env` file and update any values as needed.

### 3. Start Services
```bash
make dev
```
This starts PostgreSQL, Redis, Temporal, and the Django development server.

### 4. Run Migrations
```bash
docker compose -f docker/compose.yaml exec web python src/myproject/manage.py migrate
```

### 5. Create a Superuser
```bash
docker compose -f docker/compose.yaml exec web python src/myproject/manage.py createsuperuser
```

### 6. Access the Application
- **Django Admin:** http://localhost:8000/admin/
- **Chat Interface:** http://localhost:8000/chat/
- **API Docs (Swagger):** http://localhost:8000/api/v1/docs/
- **Temporal UI:** http://localhost:8080/

<!-- TODO: Add screenshots of each page -->

## Option B: Local Development with Conda

### 1. Create the Conda Environment
```bash
conda env create -f environment.yml
conda activate myproject
```

### 2. Install the Project
```bash
pip install -e ".[test]"
```

### 3. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your local database and Redis connection strings
```

### 4. Start External Services
You still need PostgreSQL, Redis, and Temporal running. You can start just those from Docker:
```bash
docker compose -f docker/compose.yaml up -d postgres redis temporalio temporalio-ui
```

### 5. Run Migrations and Start
```bash
python src/myproject/manage.py migrate
python src/myproject/manage.py createsuperuser
python src/myproject/manage.py runserver_plus 0.0.0.0:8000
```

## Seeding Development Data

```bash
make seed
# Or: python src/myproject/manage.py seed_db
```

This creates a test user (`testuser` / `testpass123`) and any other example data.

## Running Tests

```bash
make test
# Or: python -m pytest
```

## Next Steps

- Read [Architecture](architecture.md) to understand the project structure
- Read [AI Assistant Setup](ai-assistant-setup.md) to configure the AI chat
- Read [Django Commands](django-commands.md) for available management commands
