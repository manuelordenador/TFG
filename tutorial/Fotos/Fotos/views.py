from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def fotos(request):
    return render(request, 'fotos.html', {})