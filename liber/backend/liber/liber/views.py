"""
Documento base de vistas
"""

from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

