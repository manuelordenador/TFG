from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0007_genero_materia_alter_grabacion_genero_and_more'),
    ]

    operations = [
        UnaccentExtension(),
    ]