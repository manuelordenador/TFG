from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False)
    shortDesc = models.CharField(max_length=20, blank=False, null=False)
    longDesc = models.CharField(max_length=50, blank=False, null=False)
    stock = models.IntegerField(default=20)

    def __str__(self):
        return self.name