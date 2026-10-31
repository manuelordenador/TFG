# prestamos/admin.py
from django.contrib import admin
from .models import Prestamo


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    # Columnas que se muestran en la lista
    list_display = [
        'id',
        'socio_display',
        'ejemplar_display',
        'fechaInicio',
        'fechaFin',
        'fechaDevolucion',
        'estado_prestamo',
        'prorrogasRestantes',
    ]
    
    # Filtros laterales
    list_filter = [
        'fechaInicio',
        'fechaFin',
        'fechaDevolucion',
        'prorrogasRestantes',
    ]
    
    # Búsqueda
    search_fields = [
        'socio__usuario__username',
        'socio__usuario__first_name',
        'socio__usuario__last_name',
        'socio__usuario__email',
        'socio__numSocio',
        'ejemplar__obra__titulo',
        'ejemplar__obra__signatura',
    ]
    
    # Ordenación por defecto (más recientes primero)
    ordering = ['-fechaInicio']
    
    # Campos de solo lectura (los calculados y los auto_now_add)
    readonly_fields = ['fechaInicio']
    
    # Paginación en el admin
    list_per_page = 25
    
    # Fechas jerárquicas (navegación por año/mes/día)
    date_hierarchy = 'fechaInicio'
    
    # Agrupación de campos en el formulario de edición
    fieldsets = (
        ('Información del préstamo', {
            'fields': ('socio', 'ejemplar', 'fechaInicio')
        }),
        ('Fechas', {
            'fields': ('fechaFin', 'fechaDevolucion', 'fechaProrroga')
        }),
        ('Prórrogas', {
            'fields': ('prorrogasRestantes',)
        }),
    )
    
    # --------------------------------------------------
    # Métodos para mostrar información legible
    # --------------------------------------------------
    
    @admin.display(description='Socio', ordering='socio__usuario__last_name')
    def socio_display(self, obj):
        """Muestra el nombre completo del socio y su número."""
        nombre = obj.socio.usuario.get_full_name() or obj.socio.usuario.username
        return f"{nombre} (Socio #{obj.socio.numSocio})"
    
    @admin.display(description='Ejemplar', ordering='ejemplar__idEjemplar')
    def ejemplar_display(self, obj):
        """Muestra el ejemplar con el título de la obra."""
        return f"#{obj.ejemplar.idEjemplar} - {obj.ejemplar.obra.titulo}"
    
    @admin.display(description='Estado')
    def estado_prestamo(self, obj):
        """Muestra el estado del préstamo (activo, devuelto, vencido)."""
        from django.utils import timezone
        
        if obj.fechaDevolucion:
            return '✅ Devuelto'
        
        hoy = timezone.now().date()
        if obj.fechaFin < hoy:
            return '🔴 Vencido'
        
        return '🟢 Activo'