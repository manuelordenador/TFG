# gestionUsuarios/decorators.py
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect

def es_bibliotecario(user):
    """Verifica si el usuario es bibliotecario"""
    return user.is_authenticated and user.tipo == 'BIBLIOTECARIO'

def es_admin(user):
    """Verifica si el usuario es administrador"""
    return user.is_authenticated and user.tipo == 'ADMIN'

def es_socio(user):
    """Verifica si el usuario es socio"""
    return user.is_authenticated and user.tipo == 'SOCIO'

def roles_required(*tipos_permitidos):
    """
    Decorador parametrizado que permite el acceso solo a usuarios
    autenticados cuyo `tipo` esté en la lista de tipos permitidos.
    
    Uso:
        @roles_required('ADMIN')
        @roles_required('BIBLIOTECARIO', 'ADMIN')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied
            if request.user.tipo not in tipos_permitidos:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Atajos 
admin_required = roles_required('ADMIN')
bibliotecario_required = roles_required('BIBLIOTECARIO', 'ADMIN')

def solo_invitados(view_func):
    """
    Permite el acceso solo a usuarios NO autenticados.
    Si el usuario ya está logueado, lo redirige a 'home'.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper