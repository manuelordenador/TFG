"""
Documento base de vistas de la gestión de usuarios.
"""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import *

def registro_view(request):
    if request.method == 'POST':
        form = RegistroSocioForm(request.POST)
        if form.is_valid():
            usuario = form.save() #aqui se le pasa la password hasheada a la bdd, y se descartan las passwords de texto plano
            login(request, usuario) #garantiza persistencia de sesión
            return redirect('home')
    else:
        form = RegistroSocioForm()
    return render(request, 'gestionUsuarios/registro.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        # si los campos que ha introducido el usuario son válidos:
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('home') 
    else:
        form = LoginForm()
    return render(request, 'gestionUsuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "logout OK")
    return redirect('login')

@login_required
def perfil_view(request):
    return render(request, 'gestionUsuarios/perfil.html')