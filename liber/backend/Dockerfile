# versión moderna y ligera de Python
FROM python:3.12-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalación de dependencias del sistema necesarias para PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requirements.txt primero (para aprovechar caché de Docker)
COPY requirements.txt .

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# comprobación de que todo está en orden (DEBUG)
RUN pwd && ls -l && ls -l liber

# Hacemos el script ejecutable
RUN chmod +x entrypoint.sh

# Exponemos el puerto de Django
EXPOSE 8000

# Punto de entrada
ENTRYPOINT ["./entrypoint.sh"]