# gestionUsuarios/management/commands/populate_socios.py
from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.contrib.auth.hashers import make_password
from gestionUsuarios.models import Usuario, Socio

class Command(BaseCommand):
    help = 'Puebla la tabla de socios con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--numero',
            type=int,
            default=50,
            help='Número de socios a crear (default: 50)'
        )

    def handle(self, *args, **options):
        n = options['numero']
        fake = Faker('es_ES')
        
        self.stdout.write(f'Creando {n} socios...')
        
        usuarios_creados = []
        for i in range(n):
            # 1. Crear usuario
            usuario = Usuario(
                username=f"socio_{i+1:04d}",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=make_password('password123'),
                tipo=Usuario.TipoUsuario.SOCIO,
                telefono=fake.numerify('6#########'),
                genero=random.choice([True, False]),
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            usuario.save()
            usuarios_creados.append(usuario)
            
            # 2. Crear socio vinculado
            socio = Socio(
                usuario=usuario,
                numSocio=None,  # Se genera automáticamente
                penalizado=random.choice([True, False]),
                fechaPenalizacion=fake.date_between(start_date='-30d', end_date='today') if random.choice([True, False]) else None,
                fechaBaja=None,
            )
            socio.save()
        
        self.stdout.write(self.style.SUCCESS(f'{n} socios creados exitosamente'))