# catalogo/admin.py
from django.contrib import admin
from .models import *


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['idAutor', 'nombre', 'apellidos']
    search_fields = ['nombre', 'apellidos']


@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ['idObra', 'titulo', 'tipo', 'signatura', 'fechaPublicacion']
    list_filter = ['tipo']
    search_fields = ['titulo', 'signatura']


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'isbn', 'editorial', 'materia', 'submateria']
    list_filter = ['materia', 'submateria']
    search_fields = ['titulo', 'isbn']
    
    @admin.display(description='Materia')
    def materia_display(self, obj):
        return obj.get_materia_display() or '—'
    
    @admin.display(description='Submateria')
    def submateria_display(self, obj):
        return obj.get_submateria_display() or '—'


@admin.register(Revista)
class RevistaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'issn', 'numero', 'periodicidad']
    search_fields = ['titulo', 'issn']


@admin.register(Periodico)
class PeriodicoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'issn', 'numero', 'director']
    search_fields = ['titulo', 'issn']

@admin.register(Grabacion)
class GrabacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ean', 'soporte', 'genero', 'subgenero']
    list_filter = ['soporte', 'genero', 'subgenero']
    search_fields = ['titulo', 'ean']
    
    @admin.display(description='Género')
    def genero_display(self, obj):
        return obj.get_genero_display() or '—'
    
    @admin.display(description='Subgénero')
    def subgenero_display(self, obj):
        return obj.get_subgenero_display() or '—'

@admin.register(Ejemplar)
class EjemplarAdmin(admin.ModelAdmin):
    list_display = ['idEjemplar', 'obra', 'reservado']
    search_fields = ['obra__titulo']
    
@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Submateria)
class SubmateriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'materia']
    list_filter = ['materia']
    search_fields = ['nombre']


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


@admin.register(Subgenero)
class SubgeneroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'genero']
    list_filter = ['genero']
    search_fields = ['nombre']