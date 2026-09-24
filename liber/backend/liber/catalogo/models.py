from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta

Usuario = get_user_model()  # Socio, Bibliotecario o Admin


class Autor(models.Model):
    """Autor de una(s) obra(s)"""
    idAutor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Obra(models.Model):
    """Clase abstracta base para todos los tipos de obra, no es Abstract = True
    porque sí que tiene que tener una tabla dentro de la base de datos"""
    
    idObra = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.ManyToManyField(Autor, related_name='obras') #relacion N:N
    fechaPublicacion = models.DateField(null=True, blank=True)
    signatura = models.CharField(max_length=50, unique=True)
    
    TIPO_OBRA = [
        ('LIBRO', 'Libro'),
        ('REVISTA', 'Revista'),
        ('PERIODICO', 'Periódico'),
        ('GRABACION', 'Grabación'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_OBRA)
    
    def get_autores_display(self):
        """Devuelve los primeros 3 autores como string, método pensado para mostrar información sencilla de la obra"""
        autores = self.autor.all()[:3]
        if not autores:
            return "Autor desconocido"
        return ", ".join([f"{a.nombre} {a.apellidos}" for a in autores])
    
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"
    
class Editorial(models.Model):
    """Representación de las editoriales de libros"""
    identificador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"

class Libro(Obra):
    isbn = models.CharField(max_length=13, unique=True)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, related_name='Libros')
    materia = models.CharField(max_length=255, null=True, blank=True)
    coleccion = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.tipo = 'LIBRO'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.titulo} (ISBN: {self.isbn})"

class Revista(Obra):
    issn = models.CharField(max_length=8, unique=True)
    numero = models.IntegerField(null=True, blank=True)
    volumen = models.IntegerField(null=True, blank=True)
    temporada = models.CharField(max_length=50,null=True, blank=True)
    periodicidad = models.CharField(max_length=50, null=True, blank=True)
    materia = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        self.tipo = 'REVISTA'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.titulo} - Nº{self.numero}"

class Periodico(Obra):
    issn = models.CharField(max_length=8, unique=True)
    numero = models.IntegerField(null=True, blank=True)
    edicion = models.CharField(max_length=50, null=True, blank=True)  # Geográfica/temporal
    periodicidad = models.CharField(max_length=50)
    director = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        self.tipo = 'PERIODICO'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.titulo} - Nº{self.numero}"
    
class Productora(models.Model):
    """Representación de las productoras de grabaciones"""
    identificador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"

class Grabacion(Obra):
    ean = models.CharField(max_length=13, unique=True)
    soporte = models.CharField(max_length=20, choices=[
        ('CD', 'CD'),
        ('DVD', 'DVD'),
        ('BLURAY', 'Blu-ray'),
        ('VINILO', 'Vinilo'),
        ('CASETE', 'Casete'),
        ('VHS', 'VHS')
    ])
    duracion = models.DurationField()
    productora = models.ForeignKey(Productora,on_delete=models.SET_NULL,null=True,blank=True,related_name='grabaciones')
    genero = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.tipo = 'GRABACION'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.titulo} ({self.soporte})"

class Ejemplar(models.Model):
    """Representación de cada ejemplar dentro de la biblioteca"""
    idEjemplar = models.AutoField(primary_key=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='ejemplares')
    reservado = models.BooleanField(default=False, null=False, blank=False)
    # El estado se calcula: prestado/disponible según relaciones
    
    def __str__(self):
        return f"Ejemplar #{self.idEjemplar} - {self.obra.titulo}"
    
    @property
    def estado(self):
        """Calcula si el ejemplar está prestado o disponible"""
        prestamo_activo = self.prestamos.filter(fechaDevolucion__isnull=True).first()
        if prestamo_activo:
            return "PRESTADO"
        return "DISPONIBLE"
    
class Prestamo(models.Model):
    socio = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos')
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE, related_name='prestamos')
    fechaInicio = models.DateField(auto_now_add=True)
    fechaFin = models.DateField()
    fechaDevolucion = models.DateField(null=True, blank=True)
    fechaProrroga = models.DateField(null=True, blank=True)
    prorrogasRestantes = models.IntegerField(default=3)
    
    def __str__(self):
        return f"Préstamo {self.id} - {self.socio} - {self.ejemplar}"
    
    def save(self, *args, **kwargs):
        # Lógica de fechas y prórrogas
        if not self.fechaFin:
            self.fechaFin = self.fechaInicio + timedelta(days=20)
        super().save(*args, **kwargs)