from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    # clase para decidir que atributos del modelo usuario aparecen
    class Meta:
        model = Usuario
        fields = [
            'username', 
            'first_name',
            'last_name',
            'email',
            'telefono',
            'genero']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # aqui hago obligatorios los campos necesarios
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

# en login no hace falta meter campos adicionales porque los necesarios ya los tiene abstractuser
class LoginForm(AuthenticationForm):
    pass