from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Crea un superusuario admin:admin si no existe'

    def handle(self, *args, **options):
        if Usuario.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('⚠️ El usuario "admin" ya existe. No se crea de nuevo.'))
            return

        admin = Usuario.objects.create_superuser(
            username='admin',
            email='admin@liber.local',
            password='admin',
        )
        admin.tipo = Usuario.TipoUsuario.ADMIN
        admin.save(update_fields=['tipo'])
        self.stdout.write(self.style.SUCCESS('✅ Superusuario "admin" creado (usuario: admin, contraseña: admin)'))