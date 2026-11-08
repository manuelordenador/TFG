from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from gestionUsuarios.models import Socio
from gestionUsuarios.decorators import bibliotecario_required
from catalogo.models import Ejemplar
from prestamos.models import Prestamo, DIAS_PRESTAMO, PRORROGAS_INICIALES
from .utils import comprobar_limite

@login_required
@bibliotecario_required
def prestar_ejemplar(request, pk):
    ejemplar = get_object_or_404(Ejemplar, pk=pk)
    tipo_obra = ejemplar.obra.tipo

    # 1. ¿La obra puede prestarse?
    puede, motivo = ejemplar.obra.puede_prestarse()
    if not puede:
        messages.error(request, motivo)
        return redirect('catalogo:detalle_obra', pk=ejemplar.obra.pk)

    # 2. ¿El ejemplar está disponible?
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

        # 3. ¿Está penalizado?
        if socio.esta_penalizado:
            messages.error(
                request,
                f'{socio.usuario.get_full_name()} está penalizado y no puede tomar préstamos.'
            )
            return render(request, 'prestar_ejemplar.html', {'ejemplar': ejemplar})

        # 4. ¿Ha alcanzado el límite?
        puede, _, _, motivo = comprobar_limite(socio, tipo_obra)
        if not puede:
            messages.error(request, motivo)
            return render(request, 'prestar_ejemplar.html', {'ejemplar': ejemplar})

        # 5. Crear el préstamo
        hoy = timezone.now().date()
        Prestamo.objects.create(
            socio=socio,
            ejemplar=ejemplar,
            fechaInicio=hoy,
            fechaFin=hoy + timedelta(days=DIAS_PRESTAMO),
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
        Q(usuario__first_name__unaccent__icontains=query) |
        Q(usuario__last_name__unaccent__icontains=query) |
        Q(usuario__email__unaccent__icontains=query) |
        Q(numSocio__icontains=query)
    ).select_related('usuario').order_by('usuario__last_name', 'usuario__first_name')[:10]
    
    data = [
        {
            'id': socio.pk,
            'nombre': socio.usuario.get_full_name() or socio.usuario.username,
            'numSocio': socio.numSocio,
            'email': socio.usuario.email,
            'penalizado': socio.esta_penalizado,
            'texto': f"{socio.usuario.get_full_name() or socio.usuario.username} (Correo: {socio.usuario.email})",
        }
        for socio in socios
    ]
    
    return JsonResponse({'socios': data})

@login_required
@bibliotecario_required
def devolver_ejemplar(request, pk):
    """
    Marca un préstamo como devuelto (fechaDevolucion = hoy).
    Solo si el préstamo está activo (fechaDevolucion__isnull=True).
    """
    prestamo = get_object_or_404(Prestamo, pk=pk)
    socio = prestamo.socio
    # url a la que volver tras la devolución
    next_url = request.POST.get('next') or request.GET.get('next')
    
    def _redirect_back():
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect('catalogo:detalle_obra', pk=prestamo.ejemplar.obra.pk)
    
    # Verificar que el préstamo está activo
    if prestamo.fechaDevolucion is not None:
        messages.error(request, f'El préstamo #{prestamo.pk} ya fue devuelto.')
        return _redirect_back('catalogo:detalle_obra', pk=prestamo.ejemplar.obra.pk)

    if request.method == 'POST':
        hoy = timezone.now().date()

        prestamo.fechaDevolucion = hoy
        prestamo.save()

        tarde = hoy > prestamo.fechaFin
        # aplicar castigo según caso
        if tarde and socio.numCaducados == 0:
            socio.estado_penalizacion = Socio.EstadoPenalizacion.TEMPORAL
            socio.fechaPenalizacion = hoy
            socio.save(update_fields=['estado_penalizacion', 'fechaPenalizacion'])
        elif tarde and socio.numCaducados > 0:
            socio.estado_penalizacion = Socio.EstadoPenalizacion.INDEFINIDO
            socio.fechaPenalizacion = None
            socio.save(update_fields=['estado_penalizacion', 'fechaPenalizacion'])

        messages.success(request, f'Ejemplar #{prestamo.ejemplar.idEjemplar} devuelto correctamente.')
        return _redirect_back()

    return render(request, 'devolver_ejemplar.html', {'prestamo': prestamo})
