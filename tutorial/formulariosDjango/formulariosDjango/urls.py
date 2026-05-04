from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/', views.form, name='form'),
    path('goal/', views.goal, name='goal'),
    path('widget/', views.widget, name='widget'),
    path('', include('employees.urls'))
]