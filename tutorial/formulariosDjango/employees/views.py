from django.shortcuts import render
from django.http import HttpResponse
from .forms import EmpleadoForm

def index(request):
    form = EmpleadoForm()   
    return render(request, 'index.html', {'form': form})