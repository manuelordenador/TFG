from django.urls import path
from . import views

app_name = 'prestamos'

urlpatterns = [
    path('prestar/<int:pk>/', views.prestar_ejemplar, name='prestar_ejemplar'),
    path('api/buscar-socios/', views.buscar_socios, name='buscar_socios'),
]