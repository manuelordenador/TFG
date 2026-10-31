from datetime import timedelta

from django.db import models

from catalogo.models import Ejemplar, Obra
from gestionUsuarios.models import Socio

class Prestamo(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='prestamos')
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