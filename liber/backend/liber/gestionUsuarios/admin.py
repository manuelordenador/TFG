from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Socio, Bibliotecario

class SocioInline(admin.StackedInline):
    model = Socio
    can_delete = False
    verbose_name_plural = 'Datos de Socio'

class BibliotecarioInline(admin.StackedInline):
    model = Bibliotecario
    can_delete = False
    verbose_name_plural = 'Datos de Bibliotecario'

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    inlines = [SocioInline, BibliotecarioInline]
    list_display = ['username', 'email', 'tipo', 'is_staff', 'is_superuser']
    list_filter = ['tipo', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Datos Adicionales', {'fields': ('tipo', 'telefono', 'genero')}),
    )

admin.site.register(Bibliotecario)
admin.site.register(Socio)