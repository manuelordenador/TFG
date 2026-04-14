from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html', {})

def dinamico(request, name):
    categories = ['code', 'design', 'marketing']
    context = {'name': name, 'categories' : categories}
    return render(request, 'dinamico.html', context)