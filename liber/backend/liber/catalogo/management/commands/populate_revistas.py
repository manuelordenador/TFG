# catalogo/management/commands/populate_revistas.py
from django.core.management.base import BaseCommand
from faker import Faker
import random
from catalogo.models import Revista, Autor

class Command(BaseCommand):
    help = 'Puebla la tabla de revistas con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument('--numero', type=int, default=20)

    def handle(self, *args, **options):
        n = options['numero']
        fake = Faker('es_ES')
        
        self.stdout.write(f'Creando {n} revistas...')
        
        autores = list(Autor.objects.all())
        materias = ['Ciencia', 'Historia', 'Arte', 'Tecnología', 'Literatura']
        periodicidades = ['Mensual', 'Trimestral', 'Semanal', 'Anual']
        
        for i in range(n):
            revista = Revista(
                titulo=fake.catch_phrase(),
                fechaPublicacion=fake.date_between(start_date='-10y', end_date='today'),
                signatura=f"REV-{i+1:05d}",
                tipo='REVISTA',
                issn=fake.numerify('########'),
                numero=random.randint(1, 200),
                volumen=random.randint(1, 50),
                temporada=random.choice(['Primavera', 'Verano', 'Otoño', 'Invierno']),
                periodicidad=random.choice(periodicidades),
                materia=random.choice(materias),
            )
            revista.save()
            
            if autores:
                num_autores = random.randint(1, min(2, len(autores)))
                revista.autor.add(*random.sample(autores, num_autores))
        
        self.stdout.write(self.style.SUCCESS(f'✅ {n} revistas creadas exitosamente'))