from django.http import HttpResponse
from django.shortcuts import render
from .forms import ComentarioForm
from .forms import ContactForm

def form(request):
    commentform = ComentarioForm({'name': 'manuel', 'url': 'http://hola.com', 'comment': 'comentario'})
    return render(request, 'form.html', {'commentform' : commentform})

def goal(request):
    if request.method == 'GET':
        return HttpResponse('método no permitidoo')
    
    return HttpResponse(request.POST['name'])

def widget(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'widget.html', {'form': form})
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return HttpResponse("Post")
        else:
            return render(request, 'widget.html', {'form': form})