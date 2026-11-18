import os

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from prestamos.models import Prestamo


class Command(BaseCommand):
    help = 'Elimina préstamos devueltos hace más de N días'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dias',
            type=int,
            default=int(os.environ.get('DIAS_BORRADO_PRESTAMOS', 30)),
            help='Antigüedad mínima (en días) de los préstamos devueltos a borrar',
        )

    def handle(self, *args, **options):
        dias = options['dias']
        limite = timezone.now().date() - timedelta(days=dias)

        # Solo borra los que YA están devueltos y son antiguos
        qs = Prestamo.objects.filter(
            fechaDevolucion__isnull=False,
            fechaDevolucion__lt=limite,
        )

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS('No hay préstamos que borrar.'))
            return

        # Borrado en lotes para no saturar memoria/BD
        borrados = 0
        while True:
            ids = list(qs.values_list('pk', flat=True)[:1000])
            if not ids:
                break
            borrados += Prestamo.objects.filter(pk__in=ids).delete()[0]

        self.stdout.write(
            self.style.SUCCESS(f'{borrados} préstamos devueltos eliminados (>{dias} días).')
        )