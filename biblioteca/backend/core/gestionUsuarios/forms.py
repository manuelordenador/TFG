from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    # campo de confirmacion de contraseña
    passwordConfirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        label='Confirmar contraseña',
        required=True
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellidos', 'correo_e', 'contrasena', 'telefono', 'genero']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'correo_e': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (opcional)'}),
            'genero': forms.Select(
                choices=[(0, 'Hombre'), (1, 'Mujer')],
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'correo_e': 'Correo electrónico',
            'contrasena': 'Contraseña',
            'telefono': 'Teléfono',
            'genero': 'Género',
        }
        help_texts = {
            'genero': 'Seleccione el género del usuario',
        }

        def clean(self):
            cleaned_data = super().clean()
            contrasena = cleaned_data.get('contrasena')
            passwordConfirm = cleaned_data.get('passwordConfirm')

            if contrasena and passwordConfirm and contrasena != passwordConfirm:
                raise forms.ValidationError('Las contraseñas no coinciden')
            
            return cleaned_data
        
        def save(self, commit=True):
            user = super().save(commit=False)
            # se podría encriptar por aquí la contraseña
            if commit:
                user.save()
            return user