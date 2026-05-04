from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('landing/', views.landing, name='landing'),
    path('dinamico/<str:name>', views.dinamico, name='dinamico')
]
