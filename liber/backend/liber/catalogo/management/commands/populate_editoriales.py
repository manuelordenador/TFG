# catalogo/management/commands/populate_editoriales.py
from django.core.management.base import BaseCommand
from catalogo.models import Editorial

class Command(BaseCommand):
    help = 'Puebla la tabla de editoriales con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--numero',
            type=int,
            default=15,
            help='Número de editoriales a crear (default: 15)'
        )

    def handle(self, *args, **options):
        n = options['numero']
        
        self.stdout.write(f'Creando {n} editoriales...')
        
        editoriales = [
            'Alfaguara', 'Anaya', 'Planeta', 'Santillana',
            'Espasa', 'Destino', 'Tusquets', 'Seix Barral',
            'Anagrama', 'Cátedra', 'Gredos', 'Alianza Editorial',
            'Crítica', 'Akal', 'Síntesis', 'Pirámide',
            'McGraw-Hill', 'Pearson', 'Oxford University Press',
            'Cambridge University Press',
        ]
        
        for i in range(n):
            if i < len(editoriales):
                nombre = editoriales[i]
            else:
                nombre = f"Editorial {i+1}"
            
            Editorial.objects.get_or_create(nombre=nombre)
        
        self.stdout.write(self.style.SUCCESS(f'✅ {n} editoriales creadas exitosamente'))