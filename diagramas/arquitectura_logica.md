# Arquitectura lógica

Este diagrama describe las responsabilidades y dependencias entre los módulos de Liber, sin representar equipos, contenedores ni redes.

```mermaid
flowchart TB
    actor["Socio, bibliotecario<br/>o administrador"]
    interfaz["Interfaz web<br/>plantillas Django y estáticos"]
    urls["Enrutamiento del proyecto<br/>liber.urls"]
    middleware["Middleware Django<br/>sesión, autenticación,<br/>CSRF y mensajes"]
    nucleo["Módulo liber<br/>página principal y administración"]

    subgraph aplicaciones["Módulos funcionales"]
        usuarios["gestionUsuarios<br/>registro, inicio de sesión,<br/>perfiles y roles<br/><br/>Usuario, Socio y Bibliotecario"]
        catalogo["catalogo<br/>obras, autores, ejemplares<br/>y entidades editoras<br/><br/>Libro, Revista, Periódico,<br/>Grabación y Ejemplar"]
        prestamos["prestamos<br/>préstamo, devolución,<br/>prórroga y reglas de préstamo<br/><br/>Prestamo"]
    end

    orm["ORM de Django"]
    datos[("Modelos relacionales<br/>y datos persistidos")]
    tarea["Tarea programada<br/>limpiar_prestamos"]

    actor -->|"solicita una operación"| interfaz
    interfaz --> urls
    urls --> middleware
    middleware --> nucleo
    middleware --> usuarios
    middleware --> catalogo
    middleware --> prestamos

    usuarios -->|"autenticación y datos de Socio"| prestamos
    prestamos -->|"consulta disponibilidad y Ejemplar"| catalogo
    nucleo --> orm
    usuarios --> orm
    catalogo --> orm
    prestamos --> orm
    orm <-->|"lectura y escritura"| datos

    tarea -->|"elimina préstamos devueltos antiguos"| prestamos
    prestamos -->|"respuesta renderizada"| interfaz
    usuarios -->|"respuesta renderizada"| interfaz
    catalogo -->|"respuesta renderizada"| interfaz
    nucleo -->|"respuesta renderizada"| interfaz
```

Una petición llega al enrutador del proyecto y pasa por los middlewares comunes de Django. A partir de la URL se ejecuta una vista del módulo correspondiente. Las vistas coordinan formularios, permisos y reglas de negocio, y acceden a los modelos mediante el ORM; después devuelven una página renderizada al navegador.

`gestionUsuarios` proporciona la identidad y los perfiles de socio o bibliotecario. `catalogo` gestiona las obras y sus ejemplares. `prestamos` usa los datos del socio y del ejemplar para aplicar las operaciones y restricciones de circulación. La tarea programada ejecuta el comando de limpieza de préstamos devueltos antiguos y persiste sus cambios usando las mismas reglas y modelos.
