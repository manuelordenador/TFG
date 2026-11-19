#!/bin/sh
set -e

echo "Esperando a PostgreSQL..."
while ! nc -z db 5432; do sleep 1; done
echo "PostgreSQL listo."

echo "Recolectando estáticos..."
python manage.py collectstatic --noinput

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Arrancando Gunicorn..."
exec "$@"