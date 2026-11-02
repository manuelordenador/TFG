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