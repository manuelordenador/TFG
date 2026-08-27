from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Socio


class RegistroSocioForm(UserCreationForm):
    """Formulario de registro para nuevos socios.

    Este formulario crea un nuevo usuario con tipo de socio y configura
    sus atributos básicos sin detallar la lógica interna de guardado.
    """
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

class UsuarioEditForm(forms.ModelForm):
    """Formulario de edición de datos de usuario.
    Este formulario permite actualizar información básica del usuario
    y el estado de actividad de la cuenta sin entrar en detalles de implementación.
    """

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'genero', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(choices=[(0, 'Hombre'), (1, 'Mujer')], attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'genero': 'Género',
            'is_active': 'Cuenta activa',
        }