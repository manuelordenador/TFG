from django.shortcuts import render
from django.http import HttpResponse
from .models import Comment

def test(request):
    return HttpResponse("Funciona OK")

def create(request):
    # comment = Comment(name="Juanjo", score=5, comment="Me parece fatal")
    # comment.save()
    comment = Comment.objects.create(name="alex")
    return HttpResponse("Ruta creación")

def delete(request):
    # obj = Comment.objects.get(id=1)
    # obj.delete()
    Comment.objects.filter(id=2).delete
    return HttpResponse("Ruta borrado")