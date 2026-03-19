#!/bin/bash
set -e

# Ensure that migrations run before the app starts.
python backend/manage.py migrate --noinput

# Collect static files (idempotent).
python backend/manage.py collectstatic --noinput

# Default to 8080 for Cloud Run.
PORT=${PORT:-8080}

# Run the Django app with Gunicorn.
exec gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT} --workers 3 --threads 4
