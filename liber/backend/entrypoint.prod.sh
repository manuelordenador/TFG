#!/bin/bash
set -e

echo "Esperando a PostgreSQL..."
while ! nc -z db 5432; do sleep 1; done
echo "PostgreSQL listo."

# Migraciones y estáticos
python liber/manage.py migrate --noinput
python liber/manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
exec gunicorn liber.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 60