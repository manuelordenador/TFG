from django.db import models


class Usuario(models.Model):
    # Definición base de Usuario
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=255)
    correo_e = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    telefono = models.IntegerField(null=True, blank=True)
    genero = models.BooleanField(help_text="0=H, 1=M")

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# Create your models here.
