from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # OPAC principal
    path('', views.catalogo_home, name='catalogo_home'),
    # Obras
    path('obras/', views.lista_obras, name='lista_obras'),
    path('obras/<int:pk>/', views.detalle_obra, name='detalle_obra'),
    # Autores
    path('autores/', views.lista_autores, name='lista_autores'),
    path('autores/<int:pk>/', views.detalle_autor, name='detalle_autor'),
    path('registrar/', views.registrar_ejemplar, name='registrar_ejemplar'),
    path('api/buscar-autores/', views.buscar_autores, name='buscar_autores'),
    path('api/buscar-editoriales/', views.buscar_editoriales, name='buscar_editoriales'),
    path('api/buscar-productoras/', views.buscar_productoras, name='buscar_productoras'),
]