# TFG
Este es el repositorio donde se encontrará el proyecto de mi Trabajo de Fin de Grado, un sistema de gestión de bibliotecas.
De momento está en construcción

## Configuración y secretos para el despliegue

La plantilla de variables está en `liber/.env.example`. Desde la carpeta `liber`, crea los archivos locales a partir de ella y edítalos:

```powershell
Copy-Item .env.example .env
Copy-Item .env.example .env.prod
```

En Linux o macOS se puede usar `cp .env.example .env` y `cp .env.example .env.prod`. No compartas estos archivos de configuración reales: `.env` y `.env.prod` deben contener únicamente valores locales y están excluidos por `.gitignore`. Comparte solo `.env.example`, con valores ficticios y sin credenciales.

Antes de arrancar, revisa como mínimo:

- `SECRET_KEY`: sustituye `tupasswordaqui` por una clave aleatoria distinta para cada instalación. Puedes generarla con Python: `python -c "import secrets; print(secrets.token_urlsafe(50))"`. No la reutilices ni la publiques.
- `DB_PASSWORD` y `POSTGRES_PASSWORD`: usa una contraseña segura y el mismo valor en ambas variables. Haz coincidir también `DB_NAME` con `POSTGRES_DB` y `DB_USER` con `POSTGRES_USER`.
- `DEBUG`: déjalo en `False` para producción. La alternativa comentada `# DEBUG=True` es solo para desarrollo local.
- `ALLOWED_HOSTS`: indica los nombres de host permitidos, separados por comas y sin `http://` ni `https://`.
- `CSRF_TRUSTED_ORIGINS`: indica los orígenes completos, con protocolo (`https://` en producción), separados por comas. Las alternativas comentadas del ejemplo sirven para elegir los valores apropiados para local o producción. Mantén estas variables sincronizadas con el dominio configurado en Nginx.
- `STATIC_ROOT`: en producción debe coincidir con la ruta del volumen de archivos estáticos (`/vol/web/static` en la configuración actual).
- `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD`: son las credenciales SMTP. Si usas Gmail, utiliza una contraseña de aplicación, no la contraseña habitual de la cuenta.
- `PGADMIN_DEFAULT_EMAIL` y `PGADMIN_DEFAULT_PASSWORD`: solo corresponden a pgAdmin de desarrollo; no publiques sus credenciales ni expongas pgAdmin en producción.

Algunas variables del ejemplo tienen alternativas comentadas. Descomenta y utiliza solo la opción correspondiente a tu entorno; no dejes valores de ejemplo ni dos valores activos para la misma variable.

### DuckDNS y certificados HTTPS en producción

Para el despliegue de producción con DuckDNS:

1. Crea una cuenta en DuckDNS y registra el subdominio que utilizarás. Configura su DNS para que apunte al servidor de producción.
2. Copia el token de DuckDNS y guárdalo como `DUCKDNS_TOKEN` en `liber/.env.prod`. Define también `DUCKDNS_DOMAIN` y `CERTBOT_EMAIL`. No pongas valores reales en `.env.example` ni compartas `.env.prod`.
3. El servicio Certbot del Compose usa esas variables para solicitar el certificado al arrancar. Desde `liber`, inicia producción así:

   ```powershell
   docker compose --env-file .env.prod -f docker-compose.prod.yml up --build -d
   ```

   `--env-file .env.prod` es necesario para que Compose sustituya `${DUCKDNS_DOMAIN}` y `${CERTBOT_EMAIL}` en la configuración. Nginx espera a que Certbot termine correctamente antes de arrancar. `--keep-until-expiring` evita volver a emitir un certificado que todavía sea válido; no configura una tarea periódica de renovación.
4. Nginx espera encontrar `fullchain.pem` y `privkey.pem` en `/etc/letsencrypt/live/liberapp.duckdns.org/`. Si utilizas otro subdominio, configura el mismo dominio en `DUCKDNS_DOMAIN`, `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`, y actualiza `server_name` y las rutas del certificado en `liber/nginx/prod.conf`.

Los certificados deben obtenerse mediante Certbot; no inventes ni compartas claves privadas. No subas archivos `.pem`, especialmente `privkey.pem`, ni el contenido del directorio de certificados.

### Qué se puede compartir

Se pueden subir el código fuente, las migraciones, la documentación y una plantilla `.env.example` cuyos valores sean claramente ficticios. No subas `.env`, `.env.prod`, tokens de DuckDNS, claves Django, contraseñas, claves privadas o certificados PEM, volcados de base de datos ni copias de seguridad con datos reales.

Antes de publicar, revisa también el historial: el archivo auxiliar `liber/docker command` contenía un token de DuckDNS. Revócalo y sustitúyelo; si llegó a un commit o a GitHub, eliminar el archivo no elimina el token del historial.