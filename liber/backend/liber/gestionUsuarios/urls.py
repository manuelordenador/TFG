from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # lógica de inicio de sesión
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    # lógica de visionado y edición de datos
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'), 
]
