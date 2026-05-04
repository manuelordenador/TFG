from django.shortcuts import render
from django.http import HttpResponse
from .models import Articulo, Publicacion

def create(request):
    # art1 = Articulo(titular="me llamo manuel y eso")
    # art2 = Articulo(titular="me llamo manuel y eso")
    # art3 = Articulo(titular="me llamo manuel y eso")

    # art1.save()
    # art2.save()
    # art3.save()

    # pub1 = Publicacion(titulo="soy la primera publicacion")
    # pub2 = Publicacion(titulo="soy la segunda publicacion")
    # pub3 = Publicacion(titulo="soy la terceraa publicacion")
    # pub4 = Publicacion(titulo="soy la cuarta publicacion")
    # pub5 = Publicacion(titulo="soy la quinta publicacion")
    # pub6 = Publicacion(titulo="soy la sexta publicacion")
    # pub7 = Publicacion(titulo="soy la septima publicacion")
    
    # pub1.save()
    # pub2.save()
    # pub3.save()
    # pub4.save()
    # pub5.save()
    # pub6.save()
    # pub7.save()

    # art1.publicaciones.add(pub1)
    # art1.publicaciones.add(pub3)
    # art2.publicaciones.add(pub1)
    # art3.publicaciones.add(pub5)
    # art3.publicaciones.add(pub3)
    # art2.publicaciones.add(pub7)
    # art2.publicaciones.add(pub6)
    # art1.publicaciones.add(pub6)
    # art3.publicaciones.add(pub6)

    # result = art1.publicaciones.all()
    pub1 = Publicacion.objects.get(id=1)

    result = pub1.articulo_set.all()

    return HttpResponse(result)