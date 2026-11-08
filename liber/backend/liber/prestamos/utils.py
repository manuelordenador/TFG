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

def comprobar_limite(socio, tipo_obra):
    """
    Devuelve (puede, activos, limite, motivo).
    - puede: True/False
    - activos: número de préstamos activos del tipo
    - limite: límite configurado (o None si no hay)
    - motivo: mensaje de error (o None)
    """

    from .models import Prestamo, LIMITES_POR_TIPO

    limite = LIMITES_POR_TIPO.get(tipo_obra)
    if limite is None:
        return True, 0, None, None

    activos = Prestamo.objects.filter(
        socio=socio,
        fechaDevolucion__isnull=True,
        ejemplar__obra__tipo=tipo_obra,
    ).count()

    if activos >= limite:
        return False, activos, limite, (
            f'Ya tiene {activos} préstamo(s) activo(s) de tipo {tipo_obra} '
            f'(límite: {limite}).'
        )
    return True, activos, limite, None