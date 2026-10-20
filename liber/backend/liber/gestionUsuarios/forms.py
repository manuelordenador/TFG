from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Socio, Bibliotecario


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
        
class UsuarioFormBase(forms.ModelForm):
    """Campos comunes compartidos entre configuración propia y edición admin."""
    
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'genero']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(
                choices=[('', '---------'), (0, 'Hombre'), (1, 'Mujer')],
                attrs={'class': 'form-select'}
            ),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'genero': 'Género',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            existe = Usuario.objects.filter(
                email__iexact=email
            ).exclude(pk=self.instance.pk).exists()
            if existe:
                raise forms.ValidationError('Ya existe otro usuario con este correo electrónico.')
        return email


class ConfiguracionCuentaBaseForm(UsuarioFormBase):
    """Formulario para que el usuario edite SU propia cuenta."""
    pass  # Solo hereda los campos comunes


class UsuarioEditForm(UsuarioFormBase):
    """Formulario para que bibliotecarios/admin editen a otros usuarios."""
    
    class Meta(UsuarioFormBase.Meta):
        fields = UsuarioFormBase.Meta.fields + ['username', 'is_active']
        widgets = {
            **UsuarioFormBase.Meta.widgets,
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            **UsuarioFormBase.Meta.labels,
            'username': 'Usuario',
            'is_active': 'Cuenta activa',
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            existe = Usuario.objects.filter(
                username__iexact=username
            ).exclude(pk=self.instance.pk).exists()
            if existe:
                raise forms.ValidationError('Ya existe otro usuario con este nombre de usuario.')
        return username
    
class ConfiguracionBibliotecarioForm(forms.ModelForm):
    """Formulario para que un bibliotecario edite sus datos laborales."""
    
    class Meta:
        model = Bibliotecario
        fields = ['turno']
        widgets = {
            'turno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Mañana, Tarde, Noche',
            }),
        }
        labels = {
            'turno': 'Turno',
        }
        help_texts = {
            'turno': 'Indica el turno habitual en el que trabajas.',
        }