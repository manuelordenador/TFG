from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Definición base de Usuario
    telefono = models.IntegerField(null=True, blank=True)
    genero = models.BooleanField(null=True, blank=True, help_text="0=H, 1=M")

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# Create your models here.
