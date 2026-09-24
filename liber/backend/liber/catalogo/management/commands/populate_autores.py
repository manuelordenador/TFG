# catalogo/management/commands/populate_autores.py
from django.core.management.base import BaseCommand
from faker import Faker
from catalogo.models import Autor

class Command(BaseCommand):
    help = 'Puebla la tabla de autores con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--numero',
            type=int,
            default=30,
            help='Número de autores a crear (default: 30)'
        )

    def handle(self, *args, **options):
        n = options['numero']
        fake = Faker('es_ES')
        
        self.stdout.write(f'Creando {n} autores...')
        
        for i in range(n):
            autor = Autor(
                nombre=fake.first_name(),
                apellidos=f"{fake.last_name()} {fake.last_name()}",
            )
            autor.save()
        
        self.stdout.write(self.style.SUCCESS(f'✅ {n} autores creados exitosamente'))