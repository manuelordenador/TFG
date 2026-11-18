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
    curl \
    wget \
    netcat-openbsd \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Descargar supercronic para borrado de préstamos antiguos
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.51/supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=1692066e350a88ff4d7d6474fe3c7a6c41ec5e89 \
    SUPERCRONIC=supercronic-linux-amd64

RUN curl -fsSLO "$SUPERCRONIC_URL" \
    && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
    && chmod +x "$SUPERCRONIC" \
    && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
    && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# Copiamos requirements.txt primero (para aprovechar caché de Docker)
COPY requirements.txt .

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# comprobación de que todo está en orden (DEBUG)
RUN pwd && ls -l && ls -l liber

# copiar crontab
COPY crontab /app/crontab

# hacer script ejecutable
RUN chmod +x entrypoint.sh 

# Exponemos el puerto de Django
EXPOSE 8000

# punto de entrada para el contenedor
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]