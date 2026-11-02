from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Obra, Ejemplar, Prestamo
from gestionUsuarios.models import Socio
from gestionUsuarios.decorators import bibliotecario_required
from prestamos.models import Prestamo, DIAS_PRESTAMO, PRORROGAS_INICIALES
from .utils import puede_prestar, prestamos_activos_por_tipo


@login_required
@bibliotecario_required
def prestar_ejemplar(request, pk):
    """Vista para que bibliotecarios presten ejemplar a socio"""
    ejemplar = get_object_or_404(Ejemplar, pk=pk)
    tipo_obra = ejemplar.obra.tipo
    
    puede, motivo = ejemplar.obra.puede_prestarse()
    if not puede:
        messages.error(request, motivo)
        return redirect('catalogo:detalle_obra', pk=ejemplar.obra.pk)
    
    # Verificar disponibilidad
    if ejemplar.estado == 'PRESTADO':
        messages.error(request, f'El ejemplar #{ejemplar.idEjemplar} ya está prestado.')
        return redirect('catalogo:detalle_obra', pk=ejemplar.obra.pk)
    
    if request.method == 'POST':
        socio_id = request.POST.get('socio', '').strip()
        
        if not socio_id.isdigit():
            messages.error(request, 'Debes seleccionar un socio.')
            return render(request, 'prestar_ejemplar.html', {'ejemplar': ejemplar})
        
        try:
            socio = Socio.objects.get(pk=int(socio_id))
        except Socio.DoesNotExist:
            messages.error(request, 'El socio seleccionado no existe.')
            return render(request, 'prestar_ejemplar.html', {'ejemplar': ejemplar})
        
        # Verificar penalización
        if socio.penalizado:
            messages.error(
                request,
                f'El socio {socio.usuario.get_full_name()} está penalizado y no puede tomar préstamos.'
            )
            return render(request, 'prestar_ejemplar.html', {'ejemplar': ejemplar})
        
        
        
        puede, motivo = puede_prestar(socio, tipo_obra)
        if not puede:
            messages.error(request, motivo)
            return render(request, 'prestar_ejemplar.html', {'ejemplar': ejemplar})
        
        # Crear el préstamo
        hoy = timezone.now().date()
        fecha_fin = hoy + timedelta(days=DIAS_PRESTAMO)
        
        Prestamo.objects.create(
            socio=socio,
            ejemplar=ejemplar,
            fechaInicio=hoy,
            fechaFin=fecha_fin,
            prorrogasRestantes=PRORROGAS_INICIALES,
        )
        
        messages.success(
            request,
            f'Préstamo registrado: ejemplar #{ejemplar.idEjemplar} '
            f'de "{ejemplar.obra.titulo}" a {socio.usuario.get_full_name()}.'
        )
        return redirect('catalogo:detalle_obra', pk=ejemplar.obra.pk)
    
    return render(request, 'prestar_ejemplar.html', {'ejemplar': ejemplar})


@login_required
@bibliotecario_required
def buscar_socios(request):
    """API para buscar socios por nombre, apellidos, email o número de socio."""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'socios': []})
    
    socios = Socio.objects.filter(
        Q(usuario__first_name__icontains=query) |
        Q(usuario__last_name__icontains=query) |
        Q(usuario__email__icontains=query) |
        Q(numSocio__icontains=query)
    ).select_related('usuario').order_by('usuario__last_name', 'usuario__first_name')[:10]
    
    data = [
        {
            'id': socio.pk,
            'nombre': socio.usuario.get_full_name() or socio.usuario.username,
            'numSocio': socio.numSocio,
            'email': socio.usuario.email,
            'penalizado': socio.penalizado,
            'texto': f"{socio.usuario.get_full_name() or socio.usuario.username} (Correo: {socio.usuario.email})",
        }
        for socio in socios
    ]
    
    return JsonResponse({'socios': data})