# Arquitectura física

El diagrama representa el despliegue definido en `liber/docker-compose.yml`. El equipo anfitrión se muestra de forma genérica porque el proyecto no fija sus características físicas (procesador, memoria, sistema operativo o ubicación). Los contenedores comparten los recursos de ese equipo.

```mermaid
flowchart LR
    subgraph clientes["Dispositivos cliente"]
        persona["Socio, bibliotecario<br/>o administrador"]
        navegador["Navegador web"]
        persona --> navegador
    end

    red["Red de acceso<br/>LAN o Internet"]
    navegador <-->|"HTTP"| red

    subgraph anfitrion["Equipo anfitrión con Docker Engine"]
        puerto_web["Puerto publicado<br/>8000:8000"]
        puerto_pgadmin["Puerto publicado<br/>5050:80"]
        puerto_db["Puerto publicado<br/>5432:5432"]

        subgraph compose["Servicios de Docker Compose"]
            subgraph bridge["Red bridge interna: net"]
                web["web<br/>Django, vistas, plantillas<br/>y archivos estáticos"]
                cron["cron<br/>Supercronic y limpieza<br/>programada de préstamos"]
                pgadmin["pgAdmin 4"]
                db["db<br/>PostgreSQL 16"]
            end

            datos_db[("Volumen persistente<br/>postgres_data")]
            datos_pgadmin[("Volumen persistente<br/>pgadmin_data")]
        end

        puerto_web --> web
        puerto_pgadmin --> pgadmin
        puerto_db --> db
        web -->|"Conexión a db:5432"| db
        cron -->|"Conexión a db:5432"| db
        pgadmin -->|"Conexión de administración"| db
        db --- datos_db
        pgadmin --- datos_pgadmin
    end

    red <-->|"Puerto 8000"| puerto_web
    tecnico["Personal técnico"] -->|"Puerto 5050"| red
    herramienta["Herramienta SQL externa"] -->|"Puerto 5432 (opcional)"| red
```

La aplicación web y la tarea programada se ejecutan en contenedores distintos, pero usan la misma imagen del backend y se comunican con PostgreSQL a través de la red `net`. PostgreSQL conserva los datos en `postgres_data`; pgAdmin conserva su configuración en `pgadmin_data`. El navegador recibe páginas generadas por Django, por lo que no hay un contenedor de frontend independiente.

Los puertos publicados y la red de acceso representan la configuración de Compose; el repositorio no especifica si el servidor se encuentra en una red local o es accesible desde Internet, ni configura en Compose un proxy inverso o terminación TLS.
