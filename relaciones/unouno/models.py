from django.db import models

class Lugar(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Restaurante(models.Model):
    lugar = models.OneToOneField(Lugar, on_delete=models.CASCADE, primary_key=True)
    nEmpleados = models.IntegerField(default=1)

    def __str__(self):
        return self.lugar.name