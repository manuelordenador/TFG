from django.forms import ModelForm
from .models import Empleado

class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['name', 'last_name', 'email']