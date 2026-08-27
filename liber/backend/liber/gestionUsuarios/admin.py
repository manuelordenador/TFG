from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Socio, Bibliotecario

class SocioInline(admin.StackedInline):
    model = Socio
    can_delete = False
    verbose_name_plural = 'Datos de Socio'
    fk_name = 'usuario'

class BibliotecarioInline(admin.StackedInline):
    model = Bibliotecario
    can_delete = False
    verbose_name_plural = 'Datos de Bibliotecario'
    fk_name = 'usuario'

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    inlines = [SocioInline, BibliotecarioInline]
    list_display = ['username', 'email', 'tipo', 'is_staff', 'is_superuser']
    list_filter = ['tipo', 'is_staff']
    
    # campos para edición
    fieldsets = UserAdmin.fieldsets + (
        ('Datos Adicionales', {'fields': ('tipo', 'telefono', 'genero')}),
    )

    # campos para creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos Adicionales', {
            'fields': ('tipo', 'telefono', 'genero')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Guardar usuario y crear perfil automáticamente"""
        super().save_model(request, obj, form, change)
        
        # Crear perfil según el tipo (solo si es nuevo)
        if not change:  # Si es un usuario nuevo
            if obj.tipo == Usuario.TipoUsuario.SOCIO:
                Socio.objects.get_or_create(usuario=obj)
            elif obj.tipo == Usuario.TipoUsuario.BIBLIOTECARIO:
                Bibliotecario.objects.get_or_create(usuario=obj)
            # ADMIN no tiene perfil específico

# Registrar los modelos de perfil por separado para verlos en el admin
@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'numSocio', 'penalizado']
    search_fields = ['usuario__username', 'numSocio']
    raw_id_fields = ['usuario']

@admin.register(Bibliotecario)
class BibliotecarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'numEmpleado', 'turno']
    search_fields = ['usuario__username', 'numEmpleado']
    raw_id_fields = ['usuario']
