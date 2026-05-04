from django.db import models

class Empleado(models.Model):
    name= models.CharField()
    last_name = models.CharField()
    email = models.EmailField()

    def __str__(self):
        return self.name