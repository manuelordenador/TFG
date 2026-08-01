from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'email']

class LoginForm(AuthenticationForm):
    pass


# # formulario para manejar usuarios (de momento Create y Update)
# class UsuarioForm(forms.ModelForm):
#     # campo de confirmacion de contraseña
#     passwordConfirm = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
#         label='Confirmar contraseña',
#         required=False
#     )

#     class Meta:
#         model = Usuario
#         exclude = ['id_usuario']
#         widgets = {
#             'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
#             'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
#             'correo_e': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
#             'contrasena': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
#             'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (opcional)'}),
#             'genero': forms.Select(
#                 choices=[(0, 'Hombre'), (1, 'Mujer')],
#                 attrs={'class': 'form-control'}
#             ),
#         }
#         labels = {
#             'nombre': 'Nombre',
#             'apellidos': 'Apellidos',
#             'correo_e': 'Correo electrónico',
#             'contrasena': 'Contraseña',
#             'telefono': 'Teléfono',
#             'genero': 'Género',
#         }
#         help_texts = {
#             'genero': 'Seleccione el género del usuario',
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.pk:
#             self.fields['contrasena'].required = False
#             self.fields['contrasena'].help_text = 'Dejar en blanco para mantener la contraseña actual'

#     def clean(self):
#         cleaned_data = super().clean()
#         contrasena = cleaned_data.get('contrasena')
#         passwordConfirm = cleaned_data.get('passwordConfirm')
#         modoEdicion = self.instance and self.instance.pk

#         # si estamos en modo edición y no hay contraseña, no se valida
#         if modoEdicion and not contrasena:
#             return cleaned_data

#         # validación de que coincidan las contraseñas
#         if contrasena and passwordConfirm and contrasena != passwordConfirm:
#             raise forms.ValidationError('Las contraseñas no coinciden')
        
#         return cleaned_data
    
#     # este método serializa los datos y los guarda en la bdd
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         contrasena = self.cleaned_data.get('contrasena')
#         if contrasena:
#             # se podría encriptar por aquí la contraseña
#             user.contrasena = contrasena
#         if commit:
#             user.save()
#         return user