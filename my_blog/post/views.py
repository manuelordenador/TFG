from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Bienvenido a Mi Blog</h1><p>Blog sencillo de prueba</p>")

