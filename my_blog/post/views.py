from django.shortcuts import render
from django.http import HttpResponse
from .models import Author, Entry

def queries(request):
    # obtener todos los elementos (SELECT)
    authors = Author.objects.all()
    
    # obtener los datos filtrados por condicion (WHERE)
    filtered = Author.objects.filter(email='michele88@example.org')
    
    # obtener un solo objeto (WHERE)
    author = Author.objects.get(id=1)

    # hacer limit
    limits = Author.objects.all()[:10]

    # hacer offset
    offsets = Author.objects.all()[10:]

    # hacer ORDER BY
    orders = Author.objects.all().order_by('email')

    # hacer > O < QUE
    filtereds2 = Author.objects.filter(id__lte = 15)

    # hacer CONTAINS
    filtereds3 = Author.objects.filter(name__contains = "yes")

    return render(request ,'post/queries.html',{'authors': authors, 'filtered': filtered, 'author': author, 'limits': limits, 'offsets': offsets, 'orders': orders, 'filtereds2': filtereds2, 'filtereds3': filtereds3})

def update(request):
    author = Author.objects.get(id=1)
    author.name = "juan"
    author.email = "juanjo@demo.com"
    author.save()
    return HttpResponse("actualización OK")