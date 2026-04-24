from django.shortcuts import render
from django.http import HttpResponse
from .models import Articulo, Reportero
from datetime import date

def create(request):
    rep = Reportero(nombre='manuel', apellido='martin', email='mmcb@yopmail.com')
    rep.save()

    art1 = Articulo(titulo='la ia y el( capitalismo', fechaPub=date(2022,5,5), reportero=rep)
    art2 = Articulo(titulo='holaholahola', fechaPub=date(2022,5,5), reportero=rep)
    art3 = Articulo(titulo='lalalalaalalalal', fechaPub=date(2022,5,5), reportero=rep)
    
    art1.save()
    art2.save()
    art3.save()

    # result = art1.reportero.nombre
    result1 = rep.articulo_set.count()
    return HttpResponse(result1)