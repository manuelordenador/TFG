# catalogo/management/commands/populate_ejemplares.py
from django.core.management.base import BaseCommand
import random
from catalogo.models import Obra, Ejemplar

class Command(BaseCommand):
    help = 'Puebla la tabla de ejemplares (crea ejemplares para obras existentes)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--por-obra',
            type=int,
            default=2,
            help='Número de ejemplares por obra (default: 2)'
        )

    def handle(self, *args, **options):
        por_obra = options['por_obra']
        
        obras = Obra.objects.all()
        if not obras:
            self.stdout.write(self.style.ERROR('❌ No hay obras. Ejecuta primero los populate de obras.'))
            return
        
        self.stdout.write(f'Creando ejemplares para {obras.count()} obras...')
        
        total = 0
        for obra in obras:
            # Crear entre 1 y por_obra ejemplares por obra
            num_ejemplares = random.randint(1, por_obra)
            for _ in range(num_ejemplares):
                Ejemplar.objects.create(
                    obra=obra,
                    reservado=random.choice([True, False]),
                )
                total += 1
        
        self.stdout.write(self.style.SUCCESS(f'✅ {total} ejemplares creados exitosamente'))