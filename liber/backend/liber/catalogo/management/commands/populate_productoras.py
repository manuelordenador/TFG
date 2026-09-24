# catalogo/management/commands/populate_productoras.py
from django.core.management.base import BaseCommand
from catalogo.models import Productora

class Command(BaseCommand):
    help = 'Puebla la tabla de productoras con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument('--numero', type=int, default=15)

    def handle(self, *args, **options):
        n = options['numero']
        self.stdout.write(f'Creando {n} productoras...')
        
        productoras = [
            'Sony Music', 'Universal Music', 'Warner Music',
            'EMI', 'Verve Records', 'Blue Note', 'Columbia Records',
            'Atlantic Records', 'Decca Records', 'RCA Records',
            'Philips Records', 'Deutsche Grammophon', 'Naxos',
            'Sub Pop', 'Domino Records',
        ]
        
        for i in range(n):
            nombre = productoras[i] if i < len(productoras) else f"Productora {i+1}"
            Productora.objects.get_or_create(nombre=nombre)
        
        self.stdout.write(self.style.SUCCESS(f'✅ {n} productoras creadas exitosamente'))