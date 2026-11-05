from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Usuario(AbstractUser):
    """
    Modelo concreto principal (AUTH_USER_MODEL).
    Hereda: username, password, first_name, last_name, email, is_staff, is_superuser, date_joined.
    """
    class TipoUsuario(models.TextChoices):
        SOCIO = 'SOCIO', 'Socio'
        BIBLIOTECARIO = 'BIBLIOTECARIO', 'Bibliotecario'
        ADMIN = 'ADMIN', 'Administrador'

    class Genero(models.TextChoices):
            HOMBRE = 'H', 'Hombre'
            MUJER = 'M', 'Mujer'
            OTRO = 'O', 'Otro'
            PREFIERO_NO_DECIRLO = 'X', 'Prefiero no decirlo'
    
    tipo = models.CharField(
        max_length=20, 
        choices=TipoUsuario.choices, 
        default=TipoUsuario.SOCIO
    )
    telefono = models.CharField(max_length=20, null=True, blank=True)
    
    genero = models.CharField(
        max_length=1,
        choices=Genero.choices,
        null=True,
        blank=True,
        help_text="Género del usuario"
    )
    
    @property
    def genero_display(self):
        """Devuelve el género como texto legible (o 'Sin especificar')."""
        return self.get_genero_display() or 'Sin especificar'

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"

"""las clases bibliotecario y socio heredan de Model porque la relación que tienen con usuario a nivel 
programación es de tipo 1 a 1, se trata de wrappers de usuario, pero a nivel de base de datos se 
reflejará fielmente la jerarquía planteada originalmente"""

class Bibliotecario(models.Model):
    """Especialización para empleados de la biblioteca"""
    
    class Turno(models.TextChoices):
        MANANA = 'MANANA', 'Mañana'
        TARDE = 'TARDE', 'Tarde'
    
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        primary_key=True, 
        related_name='bibliotecario_profile'
    )
    numEmpleado = models.CharField(max_length=20, unique=True, blank=True)
    turno = models.CharField(
        max_length=10,
        choices=Turno.choices,
        blank=True,
        help_text="Turno en el que trabaja el bibliotecario"
    )

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
    
    @property
    def tiene_vencidos(self):
        """True si tiene préstamos vencidos sin devolver."""
        return self.prestamos.filter(
            fechaDevolucion__isnull=True,
            fechaFin__lt=timezone.now().date(),
        ).exists()
    
    @property
    def esta_penalizado(self):
        """
        True si el socio está penalizado AHORA.
        Orden de prioridad:
        1. Tiene vencidos sin devolver → penalizado indefinidamente.
        2. `penalizado=True` con fecha → castigo temporal hasta fechaPenalizacion + TIEMPO_CASTIGO.
        3. Resto → no penalizado.
        """
        # indefinido
        if self.tiene_vencidos:
            return True
        
        if not self.penalizado:
            return False
        
        # indefinido sin vencidos, habiendo devuelto todos
        if self.fechaPenalizacion is None:
            return False
        
        # temporal; ha caducado?
        from prestamos.models import DIAS_CASTIGO
        fin_castigo = self.fechaPenalizacion + timedelta(days=DIAS_CASTIGO)
        return timezone.now().date() < fin_castigo
    
    def penalizar_temporal(self, fecha=None):
        """Castigo con fin (devolución tardía)."""
        self.penalizado = True
        self.fechaPenalizacion = fecha or timezone.now().date()
        self.save(update_fields=['penalizado', 'fechaPenalizacion'])
        
    def despenalizar(self):
        """Quitar castigo al socio"""
        self.penalizado = False
        self.fechaPenalizacion = None
        self.save(update_fields=['penalizado', 'fechaPenalizacion'])
    
    def save(self, *args, **kwargs):
        if not self.numSocio:
            ultimo = Socio.objects.order_by('-numSocio').first()
            self.numSocio = (ultimo.numSocio + 1) if (ultimo and ultimo.numSocio) else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.username} - Socio #{self.numSocio}"