import os

def _int_env(name, default):
    """
    Lee una variable de entorno como entero.
    Si no existe o no es un número válido, devuelve el valor por defecto.
    """
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def prestamos_activos_por_tipo(socio, tipo_obra):
    """Cuenta los préstamos activos de un socio para un tipo de obra."""
    from .models import Prestamo
    return Prestamo.objects.filter(
        socio=socio,
        fechaDevolucion__isnull=True,
        ejemplar__obra__tipo=tipo_obra,
    ).count()


def puede_prestar(socio, tipo_obra):
    """Devuelve (True, None) o (False, motivo)."""
    from .models import LIMITES_POR_TIPO
    limite = LIMITES_POR_TIPO.get(tipo_obra)
    if limite is None:
        return True, None
    
    activos = prestamos_activos_por_tipo(socio, tipo_obra)
    if activos >= limite:
        return False, (
            f'Ya tiene {activos} préstamo(s) activo(s) de tipo {tipo_obra} '
            f'(límite: {limite}).'
        )
    return True, None