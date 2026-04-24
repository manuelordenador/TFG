from django.db import models

class Reportero(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email
    


class Articulo(models.Model):
    titulo = models.CharField(max_length=254)
    fechaPub = models.DateField()
    reportero = models.ForeignKey(Reportero, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo