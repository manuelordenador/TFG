from datetime import timedelta
from django.db import models
from django.utils import timezone
from catalogo.models import Ejemplar, Obra
from gestionUsuarios.models import Socio
from .utils import _int_env

DIAS_PRESTAMO = _int_env('DIAS_PRESTAMO', 20)
PRORROGAS_INICIALES = _int_env('PRORROGAS_INICIALES', 3)
LIMITE_LIBROS = _int_env('LIMITE_LIBROS', 3)
LIMITE_GRABACIONES = _int_env('LIMITE_GRABACIONES', 2)
LIMITE_REVISTAS = _int_env('LIMITE_REVISTAS', 1)
DIAS_CASTIGO = _int_env('DIAS_CASTIGO', 1)

LIMITES_POR_TIPO = {
    'LIBRO': LIMITE_LIBROS,
    'GRABACION': LIMITE_GRABACIONES,
    'REVISTA': LIMITE_REVISTAS,
}

class Prestamo(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='prestamos')
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE, related_name='prestamos')
    fechaInicio = models.DateField(auto_now_add=True)
    fechaFin = models.DateField()
    fechaDevolucion = models.DateField(null=True, blank=True)
    fechaProrroga = models.DateField(null=True, blank=True)
    prorrogasRestantes = models.IntegerField(default=PRORROGAS_INICIALES)
    
    def __str__(self):
        return f"Préstamo {self.id} - {self.socio} - {self.ejemplar}"
    
    def save(self, *args, **kwargs):
        # Lógica de fechas y prórrogas
        if not self.fechaFin:
            inicio = self.fechaInicio or timezone.now().date()
            self.fechaFin = inicio + timedelta(days=DIAS_PRESTAMO)
        super().save(*args, **kwargs)