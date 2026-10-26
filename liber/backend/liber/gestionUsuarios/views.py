"""
Documento base de vistas de la gestión de usuarios.
"""
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, bibliotecario_required, socio_required
from .decorators import bibliotecario_required, solo_invitados
from .models import Usuario
from .forms import *

def _procesar_registro_socio(request, template_name, on_success):
    """
    Lógica común para crear un socio.
    
    Args:
        request: HttpRequest
        template_name: ruta del template a renderizar
        on_success: callable(usuario) → HttpResponse a devolver tras guardar
    
    Returns:
        HttpResponse
    """
    if request.method == 'POST':
        form = RegistroSocioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return on_success(usuario)
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegistroSocioForm()
    
    return render(request, template_name, {'form': form})

@solo_invitados
def registro_view(request):
    """Registro público: el propio usuario se da de alta y queda logueado."""
    
    def on_success(usuario):
        login(request, usuario)
        messages.success(request, '¡Bienvenido a Liber!')
        return redirect('home')
    
    return _procesar_registro_socio(
        request,
        template_name='registro.html',
        on_success=on_success,
    )


@login_required
@bibliotecario_required
def alta_socio_view(request):
    """Alta de socio por bibliotecario/admin."""
    
    def on_success(usuario):
        messages.success(
            request,
            f'Socio {usuario.get_full_name() or usuario.username} creado correctamente.'
        )
        return redirect('gestionUsuarios:lista_usuarios')
    
    return _procesar_registro_socio(
        request,
        template_name='alta_socio.html',
        on_success=on_success,
    )
    
@login_required
@admin_required
def crear_bibliotecario_view(request):
    if request.method == 'POST':
        form = RegistroBibliotecarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Bibliotecario {usuario.username} creado.')
            return redirect('gestionUsuarios:lista_usuarios')
    else:
        form = RegistroBibliotecarioForm()
    return render(request, 'crear_bibliotecario.html', {'form': form})

@solo_invitados
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
    return redirect('gestionUsuarios:login')

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
            return redirect('gestionUsuarios:lista_usuarios')
    else:
        messages.error(request, 'No tienes permiso para editar usuarios.')
        return redirect('gestionUsuarios:lista_usuarios')

    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario_a_editar)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario_a_editar.username} actualizado correctamente.')
            return redirect('gestionUsuarios:detalle_usuario', pk=usuario_a_editar.pk)
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
            return redirect('gestionUsuarios:lista_usuarios')
    else:
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
        return redirect('gestionUsuarios:lista_usuarios')
    
    # Prevenir autoeliminación de usuario
    if request.user.pk == usuario_a_eliminar.pk:
        messages.error(request, 'No puedes eliminarte a ti mismo.')
        return redirect('gestionUsuarios:lista_usuarios')
    
    # eliminación de usuario
    if request.method == 'POST':
        nombre_usuario = usuario_a_eliminar.get_full_name() or usuario_a_eliminar.username
        usuario_a_eliminar.delete()
        messages.success(request, f'Usuario {nombre_usuario} eliminado correctamente.')
        return redirect('gestionUsuarios:lista_usuarios')
    
    return render(request, 'eliminar_usuario.html', {
        'usuario': usuario_a_eliminar,
        'titulo': 'Confirmar eliminación'
    })
    
@login_required
@socio_required
def baja_cuenta(request):
    if request.method == 'POST':
        usuario = request.user
        logout(request)
        usuario.delete()
        return redirect('home')
    
    return redirect('gestionUsuarios:configuracion_cuenta')

@login_required
def configuracion_cuenta(request):
    """
    Vista para que cualquier usuario autenticado (socio, bibliotecario o admin)
    edite sus datos personales. Los campos específicos se muestran según el tipo.
    """
    usuario = request.user

    es_bibliotecario = (
        usuario.tipo == 'BIBLIOTECARIO'
        and hasattr(usuario, 'bibliotecario_profile')
    )
    es_socio = (
        usuario.tipo == 'SOCIO'
        and hasattr(usuario, 'socio_profile')
    )
    es_admin = usuario.tipo == 'ADMIN'

    if request.method == 'POST':
        form = ConfiguracionCuentaBaseForm(request.POST, instance=usuario)

        form_bibliotecario = None
        if es_bibliotecario:
            form_bibliotecario = ConfiguracionBibliotecarioForm(
                request.POST,
                instance=usuario.bibliotecario_profile
            )

        # Validar todos los formularios que existan
        forms_validos = form.is_valid()
        if form_bibliotecario is not None:
            forms_validos = forms_validos and form_bibliotecario.is_valid()

        if forms_validos:
            form.save()
            if form_bibliotecario is not None:
                form_bibliotecario.save()
            messages.success(request, 'Tus datos se han actualizado correctamente.')
            return redirect('gestionUsuarios:configuracion_cuenta')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ConfiguracionCuentaBaseForm(instance=usuario)
        form_bibliotecario = None
        if es_bibliotecario:
            form_bibliotecario = ConfiguracionBibliotecarioForm(
                instance=usuario.bibliotecario_profile
            )

    # Datos de solo lectura según tipo (para mostrarlos en el template)
    datos_solo_lectura = {}
    if es_socio:
        perfil = usuario.socio_profile
        datos_solo_lectura = {
            'Número de socio': perfil.numSocio,
            'Penalizado': 'Sí' if perfil.penalizado else 'No',
            'Fecha de penalización': perfil.fechaPenalizacion.strftime('%d/%m/%Y') if perfil.fechaPenalizacion else '—',
            'Fecha de baja': perfil.fechaBaja.strftime('%d/%m/%Y') if perfil.fechaBaja else '—',
        }
    elif es_bibliotecario:
        perfil = usuario.bibliotecario_profile
        datos_solo_lectura = {
            'Número de empleado': perfil.numEmpleado,
        }

    return render(request, 'configuracion_cuenta.html', {
        'form': form,
        'form_bibliotecario': form_bibliotecario,
        'es_bibliotecario': es_bibliotecario,
        'es_socio': es_socio,
        'es_admin': es_admin,
        'datos_solo_lectura': datos_solo_lectura,
    })