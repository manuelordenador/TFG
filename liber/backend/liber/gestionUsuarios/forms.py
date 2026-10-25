from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Socio, Bibliotecario

Usuario = get_user_model()

# CONSTANTES COMPARTIDAS ENTRE USUARIOS

USUARIO_WIDGETS = {
    'username': forms.TextInput(attrs={'class': 'form-control'}),
    'first_name': forms.TextInput(attrs={'class': 'form-control'}),
    'last_name': forms.TextInput(attrs={'class': 'form-control'}),
    'email': forms.EmailInput(attrs={'class': 'form-control'}),
    'telefono': forms.TextInput(attrs={'class': 'form-control'}),
    'genero': forms.Select(attrs={'class': 'form-select'}),
}

USUARIO_LABELS = {
    'username': 'Nombre de usuario',
    'first_name': 'Nombre',
    'last_name': 'Apellidos',
    'email': 'Correo electrónico',
    'telefono': 'Teléfono',
    'genero': 'Género',
}

USUARIO_FIELDS = ['username', 'first_name', 'last_name', 'email', 'telefono', 'genero']

class RegistroUsuarioBaseForm(UserCreationForm):
    """
    Clase base para formularios de creación de usuarios.
    
    - Reutiliza widgets y labels comunes.
    - Marca first_name, last_name, email como obligatorios.
    - Implementa `_crear_perfil()` que las subclases sobrescriben.
    """
    
    # Tipo de usuario a asignar (las subclases lo sobrescriben)
    tipo_usuario = None
    # Staff (las subclases lo sobrescriben)
    es_staff = False
    
    class Meta:
        model = Usuario
        fields = USUARIO_FIELDS
        widgets = USUARIO_WIDGETS
        labels = USUARIO_LABELS
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    
    def clean_email(self):
        """Valida que el email no esté ya en uso."""
        email = self.cleaned_data.get('email')
        if email:
            qs = Usuario.objects.filter(email__iexact=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Ya existe otro usuario con este correo electrónico.')
        return email
    
    def _crear_perfil(self, usuario):
        """
        Hook para que las subclases creen el perfil asociado.
        Por defecto no hace nada.
        """
        pass
    
    def save(self, commit=True):
        with transaction.atomic():
            usuario = super().save(commit=False)
            usuario.tipo = self.tipo_usuario
            usuario.is_staff = self.es_staff
            usuario.is_superuser = False
            if commit:
                usuario.save()
                self._crear_perfil(usuario)
            return usuario

class RegistroSocioForm(RegistroUsuarioBaseForm):
    """Registro público de socio."""
    
    tipo_usuario = Usuario.TipoUsuario.SOCIO
    es_staff = False
    
    def _crear_perfil(self, usuario):
        Socio.objects.create(usuario=usuario)


class RegistroBibliotecarioForm(RegistroUsuarioBaseForm):
    """Alta de bibliotecario por un admin."""
    
    tipo_usuario = Usuario.TipoUsuario.BIBLIOTECARIO
    es_staff = True
    
    turno = forms.ChoiceField(
        choices=[('', '---------')] + list(Bibliotecario.Turno.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Turno',
        help_text='Turno habitual del bibliotecario (opcional).',
    )
    
    def _crear_perfil(self, usuario):
        Bibliotecario.objects.create(
            usuario=usuario,
            turno=self.cleaned_data.get('turno', ''),
        )
        
        
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
            'genero': forms.Select(attrs={'class': 'form-select'}), 
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
    pass  # Solo hereda los campos comunes del usuario base form


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
            'turno': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'turno': 'Turno',
        }
        help_texts = {
            'turno': 'Indica el turno habitual en el que trabajas.',
        }
        
class RegistroBibliotecarioForm(UserCreationForm):
    """Formulario para que un admin cree un bibliotecario."""
    
    turno = forms.ChoiceField(
        choices=[('', '---------')] + list(Bibliotecario.Turno.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Turno',
        help_text='Turno habitual del bibliotecario (opcional).',
    )
    
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'genero']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'genero': 'Género',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    
    def save(self, commit=True):
        with transaction.atomic():
            # 1. Crear el Usuario
            usuario = super().save(commit=False)
            usuario.tipo = Usuario.TipoUsuario.BIBLIOTECARIO
            usuario.is_staff = True
            usuario.is_superuser = False
            if commit:
                usuario.save()
            
            # 2. Crear el Bibliotecario vinculado
            #    → numEmpleado se asigna automáticamente en su save()
            bibliotecario = Bibliotecario(
                usuario=usuario,
                turno=self.cleaned_data.get('turno', ''),
            )
            if commit:
                bibliotecario.save()
            
            return usuario