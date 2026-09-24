document.addEventListener('DOMContentLoaded', function() {
    const inputBusqueda = document.getElementById('autores-busqueda');
    const sugerencias = document.getElementById('autores-sugerencias');
    const seleccionados = document.getElementById('autores-seleccionados');
    const inputIds = document.getElementById('autores-ids');
    
    let autoresSeleccionados = [];  // Array de {id, nombre}
    let timeoutId = null;
    
    // Debounce: esperar 300ms antes de buscar (evita muchas peticiones)
    inputBusqueda.addEventListener('input', function() {
        clearTimeout(timeoutId);
        const query = this.value.trim();
        
        if (query.length < 2) {
            sugerencias.style.display = 'none';
            return;
        }
        
        timeoutId = setTimeout(() => {
            buscarAutores(query);
        }, 300);
    });
    
    // Buscar autores vía AJAX
    function buscarAutores(query) {
        fetch(`/catalogo/api/buscar-autores/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                mostrarSugerencias(data.autores);
            })
            .catch(error => console.error('Error:', error));
    }
    
    // Mostrar sugerencias
    function mostrarSugerencias(autores) {
        sugerencias.innerHTML = '';
        
        // Filtrar los ya seleccionados
        const noSeleccionados = autores.filter(
            a => !autoresSeleccionados.some(s => s.id === a.id)
        );
        
        if (noSeleccionados.length === 0) {
            sugerencias.innerHTML = '<div class="list-group-item text-muted">No hay resultados</div>';
            sugerencias.style.display = 'block';
            return;
        }
        
        noSeleccionados.forEach(autor => {
            const item = document.createElement('a');
            item.href = '#';
            item.className = 'list-group-item list-group-item-action';
            item.innerHTML = `<i class="fas fa-user text-primary me-2"></i>${autor.texto}`;
            item.addEventListener('click', function(e) {
                e.preventDefault();
                agregarAutor(autor);
            });
            sugerencias.appendChild(item);
        });
        
        sugerencias.style.display = 'block';
    }
    
    // Añadir autor a la lista de seleccionados
    function agregarAutor(autor) {
        if (autoresSeleccionados.some(a => a.id === autor.id)) {
            return;  // Ya está seleccionado
        }
        
        autoresSeleccionados.push(autor);
        actualizarSeleccionados();
        actualizarInputIds();
        
        // Limpiar búsqueda
        inputBusqueda.value = '';
        sugerencias.style.display = 'none';
        inputBusqueda.focus();
    }
    
    // Actualizar la lista visual de seleccionados
    function actualizarSeleccionados() {
        seleccionados.innerHTML = '';
        
        autoresSeleccionados.forEach(autor => {
            const badge = document.createElement('span');
            badge.className = 'badge bg-primary d-flex align-items-center gap-2 p-2';
            badge.innerHTML = `
                ${autor.texto}
                <button type="button" class="btn-close btn-close-white btn-sm" 
                        onclick="eliminarAutor(${autor.id})"></button>
            `;
            seleccionados.appendChild(badge);
        });
    }
    
    // Actualizar el campo oculto con los IDs
    function actualizarInputIds() {
        inputIds.value = autoresSeleccionados.map(a => a.id).join(',');
    }
    
    // Exponer eliminarAutor globalmente
    window.eliminarAutor = function(id) {
        autoresSeleccionados = autoresSeleccionados.filter(a => a.id !== id);
        actualizarSeleccionados();
        actualizarInputIds();
    };
    
    // Cerrar sugerencias al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.position-relative')) {
            sugerencias.style.display = 'none';
        }
    });
});