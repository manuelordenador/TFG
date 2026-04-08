from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world. Estamos en el index de polls")