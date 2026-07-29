from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsuarioListView.as_view(), name='usuario_list'),
    path('<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario_detail'),
    path('nuevo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
]
