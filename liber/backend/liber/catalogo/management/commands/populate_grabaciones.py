# catalogo/management/commands/populate_grabaciones.py
from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta
from catalogo.models import Grabacion, Autor, Productora

class Command(BaseCommand):
    help = 'Puebla la tabla de grabaciones con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument('--numero', type=int, default=15)

    def handle(self, *args, **options):
        n = options['numero']
        fake = Faker('es_ES')
        
        self.stdout.write(f'Creando {n} grabaciones...')
        
        autores = list(Autor.objects.all())
        if not autores:
            self.stdout.write(self.style.ERROR('❌ No hay autores. Ejecuta primero: python manage.py populate_autores'))
            return
        
        productoras = list(Productora.objects.all())
        if not productoras:
            self.stdout.write(self.style.ERROR('❌ No hay productoras. Ejecuta primero: python manage.py populate_productoras'))
            return
        
        soportes = ['CD', 'DVD', 'BLURAY', 'VINILO', 'CASETE']
        generos = ['Rock', 'Pop', 'Jazz', 'Clásica', 'Electrónica', 'Flamenco', 'Hip-Hop']
        
        for i in range(n):
            duracion_minutos = random.randint(30, 120)
            productora_seleccionada = random.choice(productoras)
            
            grabacion = Grabacion(
                titulo=fake.catch_phrase(),
                fechaPublicacion=fake.date_between(start_date='-30y', end_date='today'),
                signatura=f"GRA-{i+1:05d}",
                tipo='GRABACION',
                ean=fake.numerify('#############'),
                soporte=random.choice(soportes),
                duracion=timedelta(minutes=duracion_minutos),
                productora=productora_seleccionada,
                genero=random.choice(generos),
            )
            grabacion.save()
            
            if autores:
                num_autores = random.randint(1, min(2, len(autores)))
                grabacion.autor.add(*random.sample(autores, num_autores))
        
        self.stdout.write(self.style.SUCCESS(f'✅ {n} grabaciones creadas exitosamente'))