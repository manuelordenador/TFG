from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad'}),
        }
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'edad': 'Edad',
        }