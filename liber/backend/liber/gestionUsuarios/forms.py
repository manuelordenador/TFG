from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Socio


class RegistroSocioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'telefono', 
            'genero'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def save(self, commit=True):
        with transaction.atomic():
            usuario = super().save(commit=False)
            usuario.tipo = Usuario.TipoUsuario.SOCIO
            usuario.is_staff = False
            if commit:
                usuario.save()
                Socio.objects.create(usuario=usuario)
        return usuario

# en login no hace falta meter campos adicionales porque los necesarios ya los tiene abstractuser
class LoginForm(AuthenticationForm):
    pass