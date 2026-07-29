from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(models.Model):
    # Definición base de Usuario
    # id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=255)
    correo_e = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    telefono = models.IntegerField(null=True, blank=True)
    genero = models.BooleanField(help_text="0=H, 1=M")

    # explicita que la tabla va a ser abstracta (no se creará en la bdd)
    class Meta:
        abstract = True


# class Socio(Usuario):
#     penalizado = models.BooleanField(help_text="0=no, 1=si")
#     fechaPenalizacion = models.DateField(null=True, blank=True)
#     fechaAlta = models.DateField(auto_now_add=True)
#     fechaBaja = models.DateField(null=True, blank=True) 
#     numSocio = models.BigAutoField(primary_key=False)  