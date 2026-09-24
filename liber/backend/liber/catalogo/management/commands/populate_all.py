# catalogo/management/commands/populate_all.py
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Puebla TODA la base de datos del catálogo de una sola vez'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Poblando catálogo completo...')
        
        call_command('populate_autores', numero=30)
        call_command('populate_editoriales', numero=30)
        call_command('populate_productoras', numero=30)
        call_command('populate_libros', numero=30)
        call_command('populate_revistas', numero=20)
        call_command('populate_periodicos', numero=10)
        call_command('populate_grabaciones', numero=15)
        call_command('populate_ejemplares', por_obra=2)
        
        self.stdout.write(self.style.SUCCESS('✅ Catálogo poblado completamente'))