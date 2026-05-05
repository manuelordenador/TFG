import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from core.models import (
    Autor, Obra, Libro, Revista, Grabacion, 
    Socio, Bibliotecario, Prestar, SoporteGrabacion
)

fake = Faker('es_ES') # Genera datos en español

class Command(BaseCommand):
    help = 'Rellena la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write("Sembrando datos...")

        # 1. Crear Autores
        autores = []
        for _ in range(10):
            a = Autor.objects.create(
                nombre=fake.first_name(),
                apellidos=fake.last_name()
            )
            autores.append(a)

        # 2. Crear Obras y Libros
        for _ in range(15):
            o = Obra.objects.create(
                titulo=fake.sentence(nb_words=3).replace(".", ""),
                signatura=f"LB-{fake.random_int(100, 999)}",
                fecha_publicacion=fake.date_between(start_date='-20y', end_date='today')
            )
            o.autores.add(random.choice(autores))
            
            # Crear el ejemplar tipo Libro
            Libro.objects.create(
                obra=o,
                isbn=fake.isbn13().replace("-", ""),
                editorial=fake.company(),
                materia=fake.word(),
                reservado=False
            )

        # 3. Crear Revistas
        for _ in range(5):
            o = Obra.objects.create(
                titulo=f"Revista {fake.word().capitalize()}",
                signatura=f"RV-{fake.random_int(100, 999)}",
            )
            Revista.objects.create(
                obra=o,
                issn=fake.ssn()[:10],
                volumen=fake.random_int(1, 10),
                numero=str(fake.random_int(2020, 2026)),
                temporada="Primavera"
            )

        # 4. Crear Usuarios (Socios y Bibliotecarios)
        socios = []
        for i in range(10):
            s = Socio.objects.create(
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                correo_e=f"socio{i}@ejemplo.com",
                contrasena="pbkdf2_sha256$...", # Password dummy
                num_socio=1000 + i,
                genero=random.choice([True, False])
            )
            socios.append(s)

        Bibliotecario.objects.create(
            nombre="Ana",
            apellidos="Admin",
            correo_e="ana@biblioteca.com",
            num_empleado=5001,
            turno="Mañana",
            genero=True
        )

        # 5. Crear algunos Préstamos
        for _ in range(8):
            ejemplar_libre = Libro.objects.filter(reservado=False).first()
            if ejemplar_libre:
                fecha_in = timezone.now().date() - timedelta(days=random.randint(1, 10))
                Prestar.objects.create(
                    socio=random.choice(socios),
                    ejemplar=ejemplar_libre,
                    fecha_inicio=fecha_in,
                    fecha_fin=fecha_in + timedelta(days=15),
                    prorrogas_restantes=3
                )
                # Marcar como reservado para simular que está prestado
                ejemplar_libre.reservado = True
                ejemplar_libre.save()

        self.stdout.write(self.style.SUCCESS('¡Base de datos sembrada con éxito!'))