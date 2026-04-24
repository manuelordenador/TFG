from django.shortcuts import render
from django.http import HttpResponse
from .models import Lugar, Restaurante

def create(request):     
    lugar = Lugar(name="lugar 1", address="dirección del lugar")
    lugar.save()

    restaurante = Restaurante(lugar=lugar, nEmpleados=10)
    restaurante.save()
    return HttpResponse(restaurante.lugar.name)