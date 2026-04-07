.PHONY: dev prod test lint migrate makemigrations shell superuser seed collectstatic clean setup-env

# Development
dev:
	docker compose -f docker/compose.yaml up -d

prod:
	docker compose -f docker/compose.yaml -f docker/compose.prod.yaml up -d --build

# Testing (uses testcontainers — no live DB needed)
test:
	DJANGO_SETTINGS_MODULE=myproject.settings.test python -m pytest --cov=src/ --cov-report=term-missing

lint:
	ruff check src/ tests/
	mypy src/

# Database
migrate:
	python src/myproject/manage.py migrate

makemigrations:
	python src/myproject/manage.py makemigrations

# Shell
shell:
	python src/myproject/manage.py shell_plus

# User management
superuser:
	python src/myproject/manage.py createsuperuser

# Data
seed:
	python src/myproject/manage.py seed_db

# Static files
collectstatic:
	python src/myproject/manage.py collectstatic --noinput

# Cleanup
clean:
	docker compose -f docker/compose.yaml down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Environment setup
setup-env:
	bash docker/scripts/setup-env.sh
