from django.http import HttpResponse

def saludo(request):
    return HttpResponse("hola que tal")

def despedida(request):
    return HttpResponse("venga hasta luego..")

def adulto(request, edad):
    if edad >= 18:
        return HttpResponse("eres mayor d edad")
    else:
        return HttpResponse("no eres mayor d edad")