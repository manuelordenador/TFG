from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo concreto principal (AUTH_USER_MODEL).
    Hereda: username, password, first_name, last_name, email, is_staff, is_superuser, date_joined.
    """
    class TipoUsuario(models.TextChoices):
        SOCIO = 'SOCIO', 'Socio'
        BIBLIOTECARIO = 'BIBLIOTECARIO', 'Bibliotecario'
        ADMIN = 'ADMIN', 'Administrador'

    tipo = models.CharField(
        max_length=20, 
        choices=TipoUsuario.choices, 
        default=TipoUsuario.SOCIO
    )
    telefono = models.CharField(max_length=20, null=True, blank=True)
    genero = models.BooleanField(null=True, blank=True, help_text="0=Hombre, 1=Mujer")

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"

"""las clases bibliotecario y socio heredan de Model porque la relación que tienen con usuario a nivel 
programación es de tipo 1 a 1, se trata de wrappers de usuario, pero a nivel de base de datos se 
reflejará fielmente la jerarquía planteada originalmente"""

class Bibliotecario(models.Model):
    """Especialización para empleados de la biblioteca"""
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='bibliotecario_profile'
    )
    numEmpleado = models.CharField(max_length=20, unique=True, blank=True)
    turno = models.CharField(max_length=50, blank=True, help_text="Ej: Mañana, Tarde")

    def save(self, *args, **kwargs):
        if not self.numEmpleado:
            ultimo = Bibliotecario.objects.order_by('-numEmpleado').first()
            if ultimo and ultimo.numEmpleado.startswith('EMP'):
                numero = int(ultimo.numEmpleado.replace('EMP', '')) + 1
                self.numEmpleado = f"EMP{numero:04d}"
            else:
                self.numEmpleado = "EMP0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - {self.numEmpleado}"


class Socio(models.Model):
    """Especialización para socios de la biblioteca"""
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='socio_profile'
    )
    numSocio = models.IntegerField(unique=True, null=True, blank=True)
    penalizado = models.BooleanField(default=False)
    fechaPenalizacion = models.DateField(null=True, blank=True)
    fechaBaja = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.numSocio:
            ultimo = Socio.objects.order_by('-numSocio').first()
            self.numSocio = (ultimo.numSocio + 1) if (ultimo and ultimo.numSocio) else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - Socio #{self.numSocio}"