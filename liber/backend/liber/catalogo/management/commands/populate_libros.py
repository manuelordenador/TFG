# catalogo/management/commands/populate_libros.py
from django.core.management.base import BaseCommand
from faker import Faker
import random
from catalogo.models import Editorial, Obra, Libro, Autor

class Command(BaseCommand):
    help = 'Puebla la tabla de libros con datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument(
            '--numero',
            type=int,
            default=30,
            help='Número de libros a crear (default: 30)'
        )

    def handle(self, *args, **options):
        n = options['numero']
        fake = Faker('es_ES')
        
        self.stdout.write(f'Creando {n} libros...')
        
        # Obtener autores existentes (necesitas ejecutar populate_autores primero)
        autores = list(Autor.objects.all())
        if not autores:
            self.stdout.write(self.style.ERROR('❌ No hay autores. Ejecuta primero: python manage.py populate_autores'))
            return
        
        editoriales = list(Editorial.objects.all())
        if not editoriales:
            self.stdout.write(self.style.ERROR('❌ No hay editoriales. Ejecuta primero: python manage.py populate_editoriales'))
            return
        
        materias = ['Novela', 'Poesía', 'Ensayo', 'Historia', 'Ciencia', 'Filosofía', 'Arte', 'Tecnología']
        
        for i in range(n):
            editorial_seleccionada = random.choice(editoriales)
            # 1. Crear obra base
            obra = Libro(
                titulo=fake.sentence(nb_words=4).replace('.', ''),
                fechaPublicacion=fake.date_between(start_date='-50y', end_date='today'),
                signatura=f"SIG-{i+1:05d}",
                tipo='LIBRO',
                isbn=fake.isbn13().replace('-', ''),
                editorial=editorial_seleccionada,
                materia=random.choice(materias),
                coleccion=fake.word().capitalize() if random.choice([True, False]) else None,
            )
            obra.save()
            
            # 2. Asociar 1-3 autores aleatorios
            num_autores = random.randint(1, min(3, len(autores)))
            autores_seleccionados = random.sample(autores, num_autores)
            obra.autor.add(*autores_seleccionados)
        
        self.stdout.write(self.style.SUCCESS(f'✅ {n} libros creados exitosamente'))