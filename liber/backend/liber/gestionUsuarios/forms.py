from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    # clase para decidir que atributos del modelo usuario aparecen
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'email']

# en login no hace falta meter campos adicionales porque los necesarios ya los tiene abstractuser
class LoginForm(AuthenticationForm):
    pass