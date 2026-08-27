# gestionUsuarios/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps

def es_bibliotecario(user):
    """Verifica si el usuario es bibliotecario"""
    return user.is_authenticated and user.tipo == 'BIBLIOTECARIO'

def es_admin(user):
    """Verifica si el usuario es administrador"""
    return user.is_authenticated and user.tipo == 'ADMIN'

def es_socio(user):
    """Verifica si el usuario es socio"""
    return user.is_authenticated and user.tipo == 'SOCIO'

def bibliotecario_required(view_func):
    """Decorador que permite acceso solo a bibliotecarios o admins"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        if request.user.tipo not in ['BIBLIOTECARIO', 'ADMIN']:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
