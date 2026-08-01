#!/bin/bash
# backend/entrypoint.sh

echo "Esperando a que PostgreSQL esté listo..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL está listo."

# ✅ Solo ejecuta migraciones si RUN_MIGRATIONS es "true"
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Ejecutando migraciones..."
    python liber/manage.py makemigrations
    python liber/manage.py migrate
else
    echo "⏭️  Saltando migraciones (RUN_MIGRATIONS=false)"
fi

echo "Iniciando servidor Django..."
exec python liber/manage.py runserver 0.0.0.0:8000