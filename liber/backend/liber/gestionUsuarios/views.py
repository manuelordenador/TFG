"""
Documento base de vistas de la gestión de usuarios.
"""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .decorators import bibliotecario_required, es_bibliotecario
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
    return render(request, 'registro.html', {'form':form})

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
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "logout OK")
    return redirect('login')

@login_required
def perfil_view(request):
    return render(request, 'perfil.html')

@login_required
@bibliotecario_required
def lista_usuarios(request):
    """Vista para obtener todos los usuarios"""
    # Obtener todos los usuarios (excluyendo superusuarios)
    usuarios = Usuario.objects.exclude(is_superuser=True)
    
    # Búsqueda
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        usuarios = usuarios.filter(
            Q(username__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda) |
            Q(email__icontains=busqueda)
        )
    
    # Paginación
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'busqueda': busqueda,
        'total_usuarios': Usuario.objects.exclude(is_superuser=True).count(),
        'titulo': 'Gestión de Usuarios',
    }
    return render(request, 'lista_usuarios.html', context)

@login_required
@bibliotecario_required
def detalle_usuario(request, pk):
    """Vista para ver información de usuario específico"""
    usuario = get_object_or_404(Usuario, pk=pk)
    
    # Obtener el perfil específico según el tipo
    perfil = None
    if hasattr(usuario, 'socio_profile'):
        perfil = usuario.socio_profile
    elif hasattr(usuario, 'bibliotecario_profile'):
        perfil = usuario.bibliotecario_profile
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
    }
    return render(request, 'detalle_usuario.html', context)

@login_required
@bibliotecario_required
def editar_usuario(request, pk):
    """Vista de edición de usuario"""
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario.username} actualizado correctamente.')
            return redirect('detalle_usuario', pk=usuario.pk)
    else:
        form = UsuarioEditForm(instance=usuario)
    
    return render(request, 'editar_usuario.html', {
        'form': form,
        'usuario': usuario,
    })