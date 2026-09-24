from django import forms
from .models import Obra, Libro, Revista, Periodico, Grabacion, Ejemplar

class ObraBaseForm(forms.ModelForm):
    """Formulario base para los campos comunes de cualquier obra"""
    
    #campo de búsqueda de autores
    autores_busqueda = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar autor...',
            'autocomplete': 'On',
            'id': 'autores-busqueda',
        }),
        label='Autores'
    )
    
    class Meta:
        model = Obra
        fields = ['titulo', 'fechaPublicacion', 'signatura']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
            'fechaPublicacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'signatura': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título',
            'autor': 'Autor',
            'fechaPublicacion': 'Fecha de publicación',
            'signatura': 'Signatura',
        }


class LibroForm(ObraBaseForm):
    """Formulario para registrar un Libro"""
    
    class Meta(ObraBaseForm.Meta):
        model = Libro
        fields = ObraBaseForm.Meta.fields + ['isbn', 'editorial', 'materia', 'coleccion']
        widgets = {
            **ObraBaseForm.Meta.widgets,
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'materia': forms.TextInput(attrs={'class': 'form-control'}),
            'coleccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            **ObraBaseForm.Meta.labels,
            'isbn': 'ISBN',
            'editorial': 'Editorial',
            'materia': 'Materia',
            'coleccion': 'Colección',
        }


class RevistaForm(ObraBaseForm):
    """Formulario para registrar una Revista"""
    
    class Meta(ObraBaseForm.Meta):
        model = Revista
        fields = ObraBaseForm.Meta.fields + ['issn', 'numero', 'volumen', 'temporada', 'periodicidad', 'materia']
        widgets = {
            **ObraBaseForm.Meta.widgets,
            'issn': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'volumen': forms.NumberInput(attrs={'class': 'form-control'}),
            'temporada': forms.TextInput(attrs={'class': 'form-control'}),
            'periodicidad': forms.TextInput(attrs={'class': 'form-control'}),
            'materia': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            **ObraBaseForm.Meta.labels,
            'issn': 'ISSN',
            'numero': 'Número',
            'volumen': 'Volumen',
            'temporada': 'Temporada',
            'periodicidad': 'Periodicidad',
            'materia': 'Materia',
        }


class PeriodicoForm(ObraBaseForm):
    """Formulario para registrar un Periódico"""
    
    class Meta(ObraBaseForm.Meta):
        model = Periodico
        fields = ObraBaseForm.Meta.fields + ['issn', 'numero', 'edicion', 'periodicidad', 'director']
        widgets = {
            **ObraBaseForm.Meta.widgets,
            'issn': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'edicion': forms.TextInput(attrs={'class': 'form-control'}),
            'periodicidad': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            **ObraBaseForm.Meta.labels,
            'issn': 'ISSN',
            'numero': 'Número',
            'edicion': 'Edición',
            'periodicidad': 'Periodicidad',
            'director': 'Director',
        }


class GrabacionForm(ObraBaseForm):
    """Formulario para registrar una Grabación"""
    
    class Meta(ObraBaseForm.Meta):
        model = Grabacion
        fields = ObraBaseForm.Meta.fields + ['ean', 'soporte', 'duracion', 'productora', 'genero']
        widgets = {
            **ObraBaseForm.Meta.widgets,
            'ean': forms.TextInput(attrs={'class': 'form-control'}),
            'soporte': forms.Select(attrs={'class': 'form-select'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
            'productora': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            **ObraBaseForm.Meta.labels,
            'ean': 'EAN',
            'soporte': 'Soporte',
            'duracion': 'Duración',
            'productora': 'Productora/Sello',
            'genero': 'Género',
        }


class EjemplarForm(forms.ModelForm):
    """Formulario para los datos del ejemplar (comunes a todos los tipos)"""
    
    class Meta:
        model = Ejemplar
        fields = ['reservado']
        widgets = {
            'reservado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'reservado': 'Reservado',
        }