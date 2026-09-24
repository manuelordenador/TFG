# catalogo/admin.py
from django.contrib import admin
from .models import Autor, Obra, Libro, Revista, Periodico, Grabacion, Ejemplar

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
    list_display = ['titulo', 'isbn', 'editorial', 'materia']
    search_fields = ['titulo', 'isbn']

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
    list_display = ['titulo', 'ean', 'soporte', 'genero']
    search_fields = ['titulo', 'ean']

@admin.register(Ejemplar)
class EjemplarAdmin(admin.ModelAdmin):
    list_display = ['idEjemplar', 'obra', 'reservado']
    search_fields = ['obra__titulo']