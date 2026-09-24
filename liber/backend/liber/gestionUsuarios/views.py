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
    # los admins pueden ver todos los usuarios
    if request.user.tipo == 'ADMIN':
        usuarios = Usuario.objects.all()
    else:
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

# gestionUsuarios/views.py
@login_required
@bibliotecario_required 
def editar_usuario(request, pk):
    """Vista de edición de usuario con control de permisos"""
    usuario_a_editar = get_object_or_404(Usuario, pk=pk)
    
    if request.user.tipo == 'ADMIN':
        pass  # ADMIN edita a cualquiera
    elif request.user.tipo == 'BIBLIOTECARIO':
        if usuario_a_editar.tipo != 'SOCIO':
            messages.error(request, 'Los bibliotecarios solo pueden editar socios.')
            return redirect('lista_usuarios')
    else:
        messages.error(request, 'No tienes permiso para editar usuarios.')
        return redirect('lista_usuarios')

    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario_a_editar)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario_a_editar.username} actualizado correctamente.')
            return redirect('detalle_usuario', pk=usuario_a_editar.pk)
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = UsuarioEditForm(instance=usuario_a_editar)

    return render(request, 'editar_usuario.html', {
        'form': form,
        'usuario': usuario_a_editar,
    })
    
@login_required
@bibliotecario_required  # Solo bibliotecarios y admins 
def eliminar_usuario(request, pk):
    usuario_a_eliminar = get_object_or_404(Usuario, pk=pk)

    # Si el usuario logueado es ADMIN puede eliminar a cualquiera
    # Si es BIBLIOTECARIO solo puede eliminar SOCIOS
    if request.user.tipo == 'ADMIN':
        pass
    elif request.user.tipo == 'BIBLIOTECARIO':
        if usuario_a_eliminar.tipo != 'SOCIO':
            messages.error(request, 'Los bibliotecarios solo pueden eliminar socios.')
            return redirect('lista_usuarios')
    else:
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
        return redirect('lista_usuarios')
    
    # Prevenir autoeliminación de usuario
    if request.user.pk == usuario_a_eliminar.pk:
        messages.error(request, 'No puedes eliminarte a ti mismo.')
        return redirect('lista_usuarios')
    
    # eliminación de usuario
    if request.method == 'POST':
        nombre_usuario = usuario_a_eliminar.get_full_name() or usuario_a_eliminar.username
        usuario_a_eliminar.delete()
        messages.success(request, f'Usuario {nombre_usuario} eliminado correctamente.')
        return redirect('lista_usuarios')
    
    return render(request, 'eliminar_usuario.html', {
        'usuario': usuario_a_eliminar,
        'titulo': 'Confirmar eliminación'
    })