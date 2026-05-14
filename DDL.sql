-- ==========================================================
-- 1. CREACIÓN DE TIPOS ENUMERADOS
-- ==========================================================
CREATE TYPE soporte_grabacion AS ENUM ('CD', 'DVD', 'VHS', 'BLU-RAY', 'CASSETTE');

-- ==========================================================
-- 2. BLOQUE DE USUARIOS (HERENCIA)
-- ==========================================================

-- Tabla Base: USUARIO
CREATE TABLE USUARIO (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    correo_e VARCHAR(255) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL, -- Se almacenará cifrada por el backend
    telefono INTEGER,
    genero BOOLEAN -- 0 = H; 1 = M 
);

-- Sub-entidad: SOCIO
CREATE TABLE SOCIO (
    id_usuario INTEGER PRIMARY KEY REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    num_socio INTEGER UNIQUE NOT NULL,
    fecha_alta DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_baja DATE,
    penalizado BOOLEAN DEFAULT FALSE,
    fecha_penalizacion DATE
);

-- Sub-entidad: BIBLIOTECARIO
CREATE TABLE BIBLIOTECARIO (
    id_usuario INTEGER PRIMARY KEY REFERENCES USUARIO(id_usuario) ON DELETE CASCADE,
    num_empleado INTEGER UNIQUE NOT NULL,
    turno VARCHAR(50) -- Mañana/Tarde
);

-- Sub-entidad: ADMIN
CREATE TABLE ADMIN (
    id_usuario INTEGER PRIMARY KEY REFERENCES USUARIO(id_usuario) ON DELETE CASCADE
);

-- ==========================================================
-- 3. BLOQUE DE CATÁLOGO (OBRAS Y EJEMPLARES)
-- ==========================================================

-- Tabla AUTOR
CREATE TABLE AUTOR (
    id_autor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(255)
);

-- Tabla OBRA (Concepto intelectual)
CREATE TABLE OBRA (
    id_obra SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    signatura VARCHAR(50) NOT NULL,
    fecha_publicacion DATE
);

-- Tabla EJEMPLAR (Soporte físico vinculado a una OBRA)
CREATE TABLE EJEMPLAR (
    id_ejemplar SERIAL PRIMARY KEY,
    id_obra INTEGER NOT NULL REFERENCES OBRA(id_obra) ON DELETE CASCADE,
    reservado BOOLEAN DEFAULT FALSE
);

-- ==========================================================
-- 4. SUB-TIPOS DE EJEMPLAR (HERENCIA)
-- ==========================================================

-- Sub-tipo: LIBRO
CREATE TABLE LIBRO (
    id_ejemplar INTEGER PRIMARY KEY REFERENCES EJEMPLAR(id_ejemplar) ON DELETE CASCADE,
    isbn VARCHAR(13) UNIQUE,
    editorial VARCHAR(255),
    materia VARCHAR(255),
    coleccion VARCHAR(255)
);

-- Sub-tipo: GRABACION
CREATE TABLE GRABACION (
    id_ejemplar INTEGER PRIMARY KEY REFERENCES EJEMPLAR(id_ejemplar) ON DELETE CASCADE,
    ean VARCHAR(16) UNIQUE,
    productora_sello VARCHAR(255),
    genero VARCHAR(255),
    soporte soporte_grabacion,
    duracion INTERVAL -- Formato hh:mm:ss compatible con Postgres
);

-- Sub-tipo: PERIODICO
CREATE TABLE PERIODICO (
    id_ejemplar INTEGER PRIMARY KEY REFERENCES EJEMPLAR(id_ejemplar) ON DELETE CASCADE,
    issn VARCHAR(10),
    numero INTEGER,
    edicion VARCHAR(255),
    periodicidad VARCHAR(255),
    director VARCHAR(255)
);

-- Sub-tipo: REVISTA
CREATE TABLE REVISTA (
    id_ejemplar INTEGER PRIMARY KEY REFERENCES EJEMPLAR(id_ejemplar) ON DELETE CASCADE,
    issn VARCHAR(10),
    volumen INTEGER,
    numero VARCHAR(16),
    temporada VARCHAR(50),
    materia VARCHAR(255)
);

-- ==========================================================
-- 5. RELACIONES N:M (TABLAS INTERMEDIAS)
-- ==========================================================

-- Relación CREAR_OBRA (Autores <-> Obras)
CREATE TABLE CREAR_OBRA (
    id_autor INTEGER REFERENCES AUTOR(id_autor) ON DELETE CASCADE,
    id_obra INTEGER REFERENCES OBRA(id_obra) ON DELETE CASCADE,
    PRIMARY KEY (id_autor, id_obra)
);

-- Relación PRESTAR (Socios <-> Ejemplares)
CREATE TABLE PRESTAR (
    id_prestamo SERIAL PRIMARY KEY,
    id_usuario_socio INTEGER NOT NULL REFERENCES SOCIO(id_usuario),
    id_ejemplar INTEGER NOT NULL REFERENCES EJEMPLAR(id_ejemplar),
    fecha_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin DATE NOT NULL,
    fecha_devolucion DATE,
    prorrogas_restantes INTEGER DEFAULT 3, -- Valor por defecto ajustable
    fecha_prorroga DATE
);