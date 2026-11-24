from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

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
    
    def puede_prestarse(self):
        """Devuelve True si la obra puede prestarse según su tipo y fecha."""
        
        if self.tipo == 'PERIODICO':
            return False, 'Los periódicos no pueden prestarse.'
        
        if self.tipo == 'REVISTA':
            if not self.fechaPublicacion:
                return False, 'La revista no tiene fecha de publicación registrada.'
            dias = (timezone.now().date() - self.fechaPublicacion).days
            if dias < 30:
                return False, f'La revista se publicó hace {dias} día(s) (mínimo 30).'
        
        return True, None
    
    
    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"
    
class Editorial(models.Model):
    """Representación de las editoriales de libros"""
    identificador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"
    
class Materia(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Materias'
    
    def __str__(self):
        return self.nombre


class Submateria(models.Model):
    nombre = models.CharField(max_length=50)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='submaterias')
    
    class Meta:
        unique_together = ('nombre', 'materia')
        ordering = ['materia', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.materia.nombre})"


class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Géneros'
    
    def __str__(self):
        return self.nombre


class Subgenero(models.Model):
    nombre = models.CharField(max_length=50)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='subgeneros')
    
    class Meta:
        unique_together = ('nombre', 'genero')
        ordering = ['genero', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.genero.nombre})"

class Libro(Obra):
        
    isbn = models.CharField(max_length=13, unique=True)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, related_name='Libros')
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    submateria = models.ForeignKey(Submateria, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
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
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True, related_name='grabaciones')
    subgenero = models.ForeignKey(Subgenero, on_delete=models.SET_NULL, null=True, blank=True, related_name='grabaciones')
    
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
    
    @property
    def prestamo_activo(self):
        """Devuelve el préstamo activo del ejemplar, o None."""
        return self.prestamos.filter(fechaDevolucion__isnull=True).first()
    
