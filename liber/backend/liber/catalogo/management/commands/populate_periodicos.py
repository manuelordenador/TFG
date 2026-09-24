# catalogo/management/commands/populate_periodicos.py
from django.core.management.base import BaseCommand
from faker import Faker
import random
from catalogo.models import Periodico, Autor

class Command(BaseCommand):
    help = 'Puebla la tabla de periódicos con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument('--numero', type=int, default=10)

    def handle(self, *args, **options):
        n = options['numero']
        fake = Faker('es_ES')
        
        self.stdout.write(f'Creando {n} periódicos...')
        
        autores = list(Autor.objects.all())
        periodicidades = ['Diario', 'Semanal', 'Quincenal']
        ediciones = ['Nacional', 'Regional', 'Local', 'Internacional']
        
        for i in range(n):
            periodico = Periodico(
                titulo=fake.company() + ' Times',
                fechaPublicacion=fake.date_between(start_date='-5y', end_date='today'),
                signatura=f"PER-{i+1:05d}",
                tipo='PERIODICO',
                issn=fake.numerify('########'),
                numero=random.randint(1, 5000),
                edicion=random.choice(ediciones),
                periodicidad=random.choice(periodicidades),
                director=fake.name(),
            )
            periodico.save()
            
            if autores:
                periodico.autor.add(random.choice(autores))
        
        self.stdout.write(self.style.SUCCESS(f'✅ {n} periódicos creados exitosamente'))