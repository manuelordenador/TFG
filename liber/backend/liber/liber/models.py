from django.db import models
from django.utils import timezone

# ==========================================================
# 1. OPCIONES PARA ENUMERADOS
# ==========================================================
# Definimos el soporte según los tipos de la BBDD
class SoporteGrabacion(models.TextChoices):
    CD = 'CD', 'CD'
    DVD = 'DVD', 'DVD'
    VHS = 'VHS', 'VHS'
    BLURAY = 'BLU-RAY', 'BLU-RAY'
    CASSETTE = 'CASSETTE', 'CASSETTE'

# ==========================================================
# 2. BLOQUE DE USUARIOS (HERENCIA)
# ==========================================================



"""
class Socio(Usuario):
    # Especialización para Socio
    num_socio = models.IntegerField(unique=True)
    fecha_alta = models.DateField(default=timezone.now)
    fecha_baja = models.DateField(null=True, blank=True)
    penalizado = models.BooleanField(default=False)
    fecha_penalizacion = models.DateField(null=True, blank=True)

class Bibliotecario(Usuario):
    # Especialización para Bibliotecario
    num_empleado = models.IntegerField(unique=True)
    turno = models.CharField(max_length=50, null=True, blank=True)

class Admin(Usuario):
    # Especialización para Admin
    pass

# ==========================================================
# 3. BLOQUE DE CATÁLOGO (OBRAS Y EJEMPLARES)
# ==========================================================

class Autor(models.Model):
    # Tabla de Autores
    id_autor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=255, null=True, blank=True)

class Obra(models.Model):
    # Concepto intelectual de la Obra
    id_obra = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    signatura = models.CharField(max_length=50)
    fecha_publicacion = models.DateField(null=True, blank=True)
    # Relación N:M que genera la tabla CREAR_OBRA
    autores = models.ManyToManyField(Autor, related_name='obras')

class Ejemplar(models.Model):
    # El soporte físico
    id_ejemplar = models.AutoField(primary_key=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='ejemplares')
    reservado = models.BooleanField(default=False)

# ==========================================================
# 4. SUB-TIPOS DE EJEMPLAR (HERENCIA)
# ==========================================================

class Libro(Ejemplar):
    # Campos específicos de Libro
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    editorial = models.CharField(max_length=255, null=True, blank=True)
    materia = models.CharField(max_length=255, null=True, blank=True)
    coleccion = models.CharField(max_length=255, null=True, blank=True)

class Grabacion(Ejemplar):
    # Campos específicos de Grabación
    ean = models.CharField(max_length=16, unique=True, null=True, blank=True)
    productora_sello = models.CharField(max_length=255, null=True, blank=True)
    genero = models.CharField(max_length=255, null=True, blank=True)
    soporte = models.CharField(max_length=20, choices=SoporteGrabacion.choices, null=True, blank=True)
    duracion = models.DurationField(null=True, blank=True)

class Periodico(Ejemplar):
    # Campos específicos de Periódico
    issn = models.CharField(max_length=10, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    edicion = models.CharField(max_length=255, null=True, blank=True)
    periodicidad = models.CharField(max_length=255, null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)

class Revista(Ejemplar):
    # Campos específicos de Revista
    issn = models.CharField(max_length=10, null=True, blank=True)
    volumen = models.IntegerField(null=True, blank=True)
    numero = models.CharField(max_length=16, null=True, blank=True)
    temporada = models.CharField(max_length=50, null=True, blank=True)
    materia = models.CharField(max_length=255, null=True, blank=True)

# ==========================================================
# 5. RELACIÓN PRESTAR
# ==========================================================

class Prestar(models.Model):
    # Registro de préstamos[cite: 1, 2]
    id_prestamo = models.AutoField(primary_key=True)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    prorrogas_restantes = models.IntegerField(default=3)
    fecha_prorroga = models.DateField(null=True, blank=True)
    """