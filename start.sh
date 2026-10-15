#!/usr/bin/env bash
set -e
echo "=== Running start.sh: applying migrations and starting Gunicorn ==="
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn medicine_project.wsgi:application --bind 0.0.0.0:${PORT:-8000}
