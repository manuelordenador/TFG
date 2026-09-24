from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Obra, Autor, Libro, Revista, Periodico, Grabacion, Ejemplar
from .forms import LibroForm, RevistaForm, PeriodicoForm, GrabacionForm
from gestionUsuarios.decorators import bibliotecario_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# mapeo de los tipos de formulario
FORMULARIOS_POR_TIPO = {
    'LIBRO': LibroForm,
    'REVISTA': RevistaForm,
    'PERIODICO': PeriodicoForm,
    'GRABACION': GrabacionForm,
}

@login_required
@bibliotecario_required
def registrar_ejemplar(request):
    """
    Vista para que bibliotecarios/admin registren un nuevo ejemplar.
    Paso 1: Elegir tipo de obra
    Paso 2: Rellenar formulario específico
    """
    tipo = request.GET.get('tipo', '')
    
    #Paso 1: Si no hay tipo, mostrar selector
    if not tipo:
        return render(request, 'seleccionar_tipo_ejemplar.html', {
            'tipos': Obra.TIPO_OBRA,
        })
    
    #Validar que el tipo es válido
    if tipo not in FORMULARIOS_POR_TIPO:
        messages.error(request, 'Tipo de ejemplar no válido.')
        return redirect('catalogo:registrar_ejemplar')
    
    FormClass = FORMULARIOS_POR_TIPO[tipo]
    
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            # 1. Guardar la obra (con el tipo correspondiente)
            obra = form.save(commit=False)
            obra.tipo = tipo
            obra.save()
            autores_ids = request.POST.get('autores', '').split(',')
            autores_ids = [int(id) for id in autores_ids if id.strip().isdigit()]
            if autores_ids:
                obra.autores.set(autores_ids)
            form.save_m2m()  # Guardar la relación N:N con autor
            
            # 2. Crear el ejemplar asociado
            Ejemplar.objects.create(obra=obra, reservado=False)
            
            messages.success(request, f'{obra.get_tipo_display()} "{obra.titulo}" registrado correctamente.')
            return redirect('catalogo:detalle_obra', pk=obra.pk)
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = FormClass()
    
    return render(request, 'registrar_ejemplar.html', {
        'form': form,
        'tipo': tipo,
        'tipo_display': dict(Obra.TIPO_OBRA).get(tipo, tipo),
    })

def catalogo_home(request):
    """Página principal del catálogo público"""
    context = {
        'total_obras': Obra.objects.count(),
        'total_autores': Autor.objects.count(),
        'total_ejemplares': Ejemplar.objects.count(),
        'ultimas_obras': Obra.objects.order_by('-idObra')[:5],
        'autores_destacados': Autor.objects.annotate(
            num_obras=Count('obras')
        ).filter(num_obras__gt=0).order_by('-num_obras')[:5],
    }
    return render(request, 'catalogo_home.html', context)


def lista_obras(request):
    """Lista todas las obras con búsqueda y filtros"""
    obras = Obra.objects.all().order_by('titulo')
    
    # Búsqueda
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        obras = obras.filter(
            Q(titulo__icontains=busqueda) |
            Q(autor__nombre__icontains=busqueda) |
            Q(autor__apellidos__icontains=busqueda) |
            Q(signatura__icontains=busqueda)
        ).distinct()
    
    # Filtro por tipo
    tipo = request.GET.get('tipo', '')
    if tipo:
        obras = obras.filter(tipo=tipo)
    
    # Paginación
    paginator = Paginator(obras, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'busqueda': busqueda,
        'tipo': tipo,
        'total_obras': obras.count(),
        'tipos': Obra.TIPO_OBRA if hasattr(Obra, 'TIPO_OBRA') else [],
    }
    return render(request, 'lista_obras.html', context)


def detalle_obra(request, pk):
    """Detalle de una obra específica"""
    obra = get_object_or_404(Obra, pk=pk)
    
    # Obtener datos específicos según el tipo
    datos_especificos = None
    if obra.tipo == 'LIBRO':
        datos_especificos = Libro.objects.filter(pk=obra.pk).first()
    elif obra.tipo == 'REVISTA':
        datos_especificos = Revista.objects.filter(pk=obra.pk).first()
    elif obra.tipo == 'PERIODICO':
        datos_especificos = Periodico.objects.filter(pk=obra.pk).first()
    elif obra.tipo == 'GRABACION':
        datos_especificos = Grabacion.objects.filter(pk=obra.pk).first()
    
    # Ejemplares de esta obra
    ejemplares = obra.ejemplares.all()
    
    context = {
        'obra': obra,
        'datos_especificos': datos_especificos,
        'ejemplares': ejemplares,
        'autores': obra.autor.all(),
    }
    return render(request, 'detalle_obra.html', context)


def lista_autores(request):
    """Lista todos los autores"""
    autores = Autor.objects.annotate(
        num_obras=Count('obras')
    ).order_by('apellidos', 'nombre')
    
    # Búsqueda
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        autores = autores.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellidos__icontains=busqueda)
        )
    
    # Paginación
    paginator = Paginator(autores, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'busqueda': busqueda,
        'total_autores': autores.count(),
    }
    return render(request, 'lista_autores.html', context)


def detalle_autor(request, pk):
    """Detalle de un autor y sus obras"""
    autor = get_object_or_404(Autor, pk=pk)
    obras = autor.obras.all().order_by('titulo')
    
    context = {
        'autor': autor,
        'obras': obras,
        'total_obras': obras.count(),
    }
    return render(request, 'detalle_autor.html', context)

@login_required
@bibliotecario_required
def buscar_autores(request):
    """API para buscar autores por nombre/apellidos (autocompletado)"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'autores': []})
    
    autores = Autor.objects.filter(
        Q(nombre__icontains=query) |
        Q(apellidos__icontains=query)
    ).order_by('apellidos', 'nombre')[:10]  # Máximo 10 resultados
    
    data = [
        {
            'id': autor.idAutor,
            'nombre': autor.nombre,
            'apellidos': autor.apellidos or '',
            'texto': f"{autor.nombre} {autor.apellidos or ''}".strip(),
        }
        for autor in autores
    ]
    
    return JsonResponse({'autores': data})