document.addEventListener('DOMContentLoaded', function () {

    /**
     * Inicializa un buscador con autocompletado
     * @param {Object} config - Configuración del buscador
     * @param {string} config.inputId - ID del input de búsqueda
     * @param {string} config.sugerenciasId - ID del contenedor de sugerencias
     * @param {string} config.seleccionadosId - ID del contenedor de seleccionados
     * @param {string} config.hiddenId - ID del campo oculto con los IDs
     * @param {string} config.apiUrl - URL de la API de búsqueda
     * @param {string} config.claveRespuesta - Clave del JSON (ej: 'autores', 'editoriales')
     * @param {string} config.claveId - Nombre del campo ID en el JSON (ej: 'id')
     * @param {string} config.claveTexto - Nombre del campo texto en el JSON (ej: 'texto')
     * @param {string} config.icono - Clase del icono FontAwesome
     * @param {boolean} config.multiple - Si permite seleccionar varios (true) o uno solo (false)
     */
    function inicializarBuscador(config) {
        const input = document.getElementById(config.inputId);
        const sugerencias = document.getElementById(config.sugerenciasId);
        const seleccionados = document.getElementById(config.seleccionadosId);
        const hidden = document.getElementById(config.hiddenId);

        if (!input || !sugerencias || !seleccionados || !hidden) {
            console.warn(`Buscador no inicializado: faltan elementos para ${config.inputId}`);
            return;
        }

        let elementosSeleccionados = [];
        let timeoutId = null;

        // Debounce: esperar 300ms antes de buscar
        input.addEventListener('input', function () {
            clearTimeout(timeoutId);
            const query = this.value.trim();

            // si texto búsqueda < 2 caracteres, no recomendar nada aún
            if (query.length < 2) {
                sugerencias.style.display = 'none';
                return;
            }

            timeoutId = setTimeout(() => buscar(query), 300);
        });

        // Buscar vía AJAX
        function buscar(query) {
            fetch(`${config.apiUrl}?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    mostrarSugerencias(data[config.claveRespuesta] || []);
                })
                .catch(error => console.error('Error:', error));
        }

        // Mostrar sugerencias
        function mostrarSugerencias(items) {
            sugerencias.innerHTML = '';

            // Filtrar los ya seleccionados
            const noSeleccionados = items.filter(
                item => !elementosSeleccionados.some(s => s.id === item[config.claveId])
            );

            if (noSeleccionados.length === 0) {
                sugerencias.innerHTML = '<div class="list-group-item text-muted">No hay resultados</div>';
                sugerencias.style.display = 'block';
                return;
            }

            noSeleccionados.forEach(item => {
                const el = document.createElement('a');
                el.href = '#';
                el.className = 'list-group-item list-group-item-action';
                el.innerHTML = `<i class="${config.icono} text-primary me-2"></i>${item[config.claveTexto]}`;
                el.addEventListener('click', function (e) {
                    e.preventDefault();
                    agregar(item);
                });
                sugerencias.appendChild(el);
            });

            sugerencias.style.display = 'block';
        }

        // Añadir elemento
        function agregar(item) {
            const id = item[config.claveId];

            // Si es single, reemplazar el anterior
            if (!config.multiple) {
                elementosSeleccionados = [];
            }

            if (elementosSeleccionados.some(a => a.id === id)) {
                return;
            }

            elementosSeleccionados.push({
                id: id,
                texto: item[config.claveTexto]
            });

            actualizarSeleccionados();
            actualizarHidden();

            input.value = '';
            sugerencias.style.display = 'none';
            input.focus();
        }

        function eliminar(id) {
            elementosSeleccionados = elementosSeleccionados.filter(a => a.id !== id);
            actualizarSeleccionados();
            actualizarHidden();
        }

        // Actualizar la lista visual
        function actualizarSeleccionados() {
            seleccionados.innerHTML = '';

            elementosSeleccionados.forEach(item => {
                const badge = document.createElement('span');
                badge.className = 'badge bg-primary d-flex align-items-center gap-2 p-2';

                // Texto
                const texto = document.createTextNode(item.texto);
                badge.appendChild(texto);

                // Botón de eliminar
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'btn-close btn-close-white btn-sm';
                btn.addEventListener('click', function () {
                    eliminar(item.id);
                });
                badge.appendChild(btn);

                seleccionados.appendChild(badge);
            });
        }

        // Actualizar el campo oculto
        function actualizarHidden() {
            hidden.value = elementosSeleccionados.map(a => a.id).join(',');
        }

        // Cerrar sugerencias al hacer clic fuera
        document.addEventListener('click', function (e) {
            if (!e.target.closest(`#${config.inputId}`) &&
                !e.target.closest(`#${config.sugerenciasId}`)) {
                sugerencias.style.display = 'none';
            }
        });
    }

    // ==========================================
    // INICIALIZAR LOS 3 BUSCADORES
    // ==========================================

    // Buscador de AUTORES (múltiple)
    inicializarBuscador({
        inputId: 'autores-busqueda',
        sugerenciasId: 'autores-sugerencias',
        seleccionadosId: 'autores-seleccionados',
        hiddenId: 'autores-ids',
        apiUrl: '/catalogo/api/buscar-autores/',
        claveRespuesta: 'autores',
        claveId: 'id',
        claveTexto: 'texto',
        icono: 'fas fa-user',
        multiple: true
    });

    // Buscador de EDITORIALES (solo uno)
    inicializarBuscador({
        inputId: 'editorial-busqueda',
        sugerenciasId: 'editorial-sugerencias',
        seleccionadosId: 'editorial-seleccionada',
        hiddenId: 'editorial-id',
        apiUrl: '/catalogo/api/buscar-editoriales/',
        claveRespuesta: 'editoriales',
        claveId: 'id',
        claveTexto: 'texto',
        icono: 'fas fa-building',
        multiple: false
    });

    // Buscador de PRODUCTORAS (solo uno)
    inicializarBuscador({
        inputId: 'productora-busqueda',
        sugerenciasId: 'productora-sugerencias',
        seleccionadosId: 'productora-seleccionada',
        hiddenId: 'productora-id',
        apiUrl: '/catalogo/api/buscar-productoras/',
        claveRespuesta: 'productoras',
        claveId: 'id',
        claveTexto: 'texto',
        icono: 'fas fa-industry',
        multiple: false
    });
});