# backend/core/gestionUsuarios/management/commands/populate_usuarios.py
# definición de comando para insertar usuarios mock en la bdd
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from gestionUsuarios.models import Usuario

class Command(BaseCommand):
    help = 'Rellena la tabla de usuarios con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=int,
            default=50,
            help='Número de usuarios a crear (default: 50)'
        )

    def handle(self, *args, **options):
        number = options['number']
        
        nombres = ['Juan', 'Maria', 'Carlos', 'Ana', 'Luis', 'Carmen', 'Jose', 'Isabel']
        apellidos = ['Garcia', 'Martinez', 'Lopez', 'Sanchez', 'Perez']
        
        usuarios = []
        for i in range(number):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            
            usuario = Usuario(
                nombre=nombre,
                apellidos=f"{apellido} {random.choice(apellidos)}",
                correo_e=f"{nombre.lower()}.{apellido.lower()}.{i}@ejemplo.com",  # {i} asegura unicidad
                contrasena=make_password('password123'),
                telefono=random.randint(600000000, 699999999) if random.choice([True, False]) else None,
                genero=random.choice([0, 1])
            )
            usuarios.append(usuario)
        
        Usuario.objects.bulk_create(usuarios)
        self.stdout.write(self.style.SUCCESS(f'✅ {number} usuarios creados exitosamente'))