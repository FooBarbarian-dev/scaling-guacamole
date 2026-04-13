#!/usr/bin/env bash
set -euo pipefail

echo "==> Waiting for PostgreSQL..."
bash docker/scripts/wait-for-it.sh "${DATABASE_HOST:-postgres}" "${DATABASE_PORT:-5432}" --timeout=30

echo "==> Running migrations..."
python src/myproject/manage.py migrate --noinput

if [ "${DJANGO_ENV:-development}" = "production" ]; then
    echo "==> Collecting static files..."
    python src/myproject/manage.py collectstatic --noinput

    echo "==> Starting Gunicorn..."
    WORKERS=${GUNICORN_WORKERS:-$(python -c "import os; print(os.cpu_count() * 2 + 1)")}
    exec gunicorn myproject.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers "$WORKERS" \
        --access-logfile - \
        --error-logfile - \
        --pythonpath src
else
    echo "==> Starting development server..."
    exec python src/myproject/manage.py runserver_plus 0.0.0.0:8000
fi
