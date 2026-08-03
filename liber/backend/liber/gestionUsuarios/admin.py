from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = [field.name for field in Usuario._meta.get_fields()
                    if field.name not in [
                        'logentry',
                        'groups',
                        'user_permissions'
                    ]]
    
    
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    fieldsets = (
            (None, {'fields': ('username', 'email', 'password')}),
            ('Permisos', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
            ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
        )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(Usuario, UsuarioAdmin)