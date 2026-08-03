from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Usuario(AbstractUser):
    # Definición base de Usuario
    
    telefono = models.IntegerField(null=True, blank=True)
    genero = models.BooleanField(null=True, blank=True, help_text="0=H, 1=M")
    
    # aqui hay grupos y permisos para más adelante, de momento están comentados porque ya se heredan de abstractuser
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='usuarios_set', #nombre del grupo
    #     blank=True,
    #     help_text='Grupos a los que pertenece este usuario',
    #     verbose_name='groups',
    # )
    # # los permisos son a nivel usuario, no a nivel grupo de usuarios
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='usuarios_user_set',
    #     help_text='Permisos de este usuario',
    #     verbose_name='user permissions',
    # )
    def __str__(self):
        return self.username

# Create your models here.
