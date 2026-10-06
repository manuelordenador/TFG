document.addEventListener('DOMContentLoaded', function () {

    /**
     * Inicializa un buscador con autocompletado
     */
    function inicializarBuscador(config) {
        const input = document.getElementById(config.inputId);
        const sugerencias = document.getElementById(config.sugerenciasId);
        const seleccionados = document.getElementById(config.seleccionadosId);
        const hidden = document.getElementById(config.hiddenId);

        if (!input || !sugerencias || !seleccionados || !hidden) {
            console.warn(`Buscador no inicializado: faltan elementos para ${config.inputId}`);
            return null;  // Devolver null si no existe el buscador
        }

        let elementosSeleccionados = [];
        let timeoutId = null;

        input.addEventListener('input', function () {
            clearTimeout(timeoutId);
            const query = this.value.trim();

            if (query.length < 2) {
                sugerencias.style.display = 'none';
                return;
            }

            timeoutId = setTimeout(() => buscar(query), 300);
        });

        function buscar(query) {
            fetch(`${config.apiUrl}?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    mostrarSugerencias(data[config.claveRespuesta] || []);
                })
                .catch(error => console.error('Error:', error));
        }

        function mostrarSugerencias(items) {
            sugerencias.innerHTML = '';

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

        function agregar(item) {
            const id = item[config.claveId];

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

        function actualizarSeleccionados() {
            seleccionados.innerHTML = '';

            elementosSeleccionados.forEach(item => {
                const badge = document.createElement('span');
                badge.className = 'badge bg-primary d-flex align-items-center gap-2 p-2';

                const texto = document.createTextNode(item.texto);
                badge.appendChild(texto);

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

        function actualizarHidden() {
            hidden.value = elementosSeleccionados.map(a => a.id).join(',');
        }

        document.addEventListener('click', function (e) {
            if (!e.target.closest(`#${config.inputId}`) &&
                !e.target.closest(`#${config.sugerenciasId}`)) {
                sugerencias.style.display = 'none';
            }
        });

        // Devolver la API pública del buscador
        return {
            agregarExterno: function (item) {
                const id = item.id;

                if (!config.multiple) {
                    elementosSeleccionados = [];
                }

                if (elementosSeleccionados.some(a => a.id === id)) {
                    return;
                }

                elementosSeleccionados.push({
                    id: id,
                    texto: item.texto
                });

                actualizarSeleccionados();
                actualizarHidden();
            }
        };
    }

    // ==========================================
    // 1. INICIALIZAR LOS 3 BUSCADORES
    //    (guardando las instancias en variables)
    // ==========================================

    const buscadorAutores = inicializarBuscador({
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

    const buscadorEditoriales = inicializarBuscador({
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

    const buscadorProductoras = inicializarBuscador({
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

    // ==========================================
    // 2. FUNCIÓN GENÉRICA PARA CREAR ENTIDADES
    // ==========================================
    function configurarModalCrear(config) {
        const btnCrear = document.getElementById(config.btnId);
        const inputNombre = document.getElementById(config.inputNombreId);
        const inputApellidos = config.inputApellidosId ? document.getElementById(config.inputApellidosId) : null;
        const errorDiv = document.getElementById(config.errorDivId);
        const modalEl = document.getElementById(config.modalId);

        if (!btnCrear || !modalEl) return;

        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

        function getCsrfToken() {
            const input = document.querySelector('[name=csrfmiddlewaretoken]');
            return input ? input.value : '';
        }

        btnCrear.addEventListener('click', function () {
            errorDiv.classList.add('d-none');
            errorDiv.textContent = '';

            const nombre = inputNombre.value.trim();
            const apellidos = inputApellidos ? inputApellidos.value.trim() : '';

            if (!nombre) {
                errorDiv.textContent = 'El nombre es obligatorio.';
                errorDiv.classList.remove('d-none');
                return;
            }

            const body = new FormData();
            body.append('nombre', nombre);
            if (inputApellidos) body.append('apellidos', apellidos);
            body.append('csrfmiddlewaretoken', getCsrfToken());

            fetch(config.apiUrl, {
                method: 'POST',
                body: body,
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                },
            })
                .then(async response => {
                    const data = await response.json();
                    if (!response.ok) {
                        throw new Error(data.error || 'Error al crear el registro.');
                    }
                    return data;
                })
                .then(data => {
                    if (config.onSuccess) {
                        config.onSuccess(data);
                    }
                    modal.hide();
                    inputNombre.value = '';
                    if (inputApellidos) inputApellidos.value = '';
                })
                .catch(error => {
                    errorDiv.textContent = error.message;
                    errorDiv.classList.remove('d-none');
                });
        });

        modalEl.addEventListener('hidden.bs.modal', function () {
            inputNombre.value = '';
            if (inputApellidos) inputApellidos.value = '';
            errorDiv.classList.add('d-none');
            errorDiv.textContent = '';
        });
    }

    // ==========================================
    // 3. CONFIGURAR LOS 3 MODALES
    //    (usando las instancias guardadas arriba)
    // ==========================================

    configurarModalCrear({
        btnId: 'btn-crear-autor',
        modalId: 'modalCrearAutor',
        inputNombreId: 'nuevo-autor-nombre',
        inputApellidosId: 'nuevo-autor-apellidos',
        errorDivId: 'modalCrearAutor-error',
        apiUrl: '/catalogo/api/crear-autor/',
        onSuccess: function (data) {
            if (buscadorAutores) {
                buscadorAutores.agregarExterno({ id: data.id, texto: data.texto });
            }
        }
    });

    configurarModalCrear({
        btnId: 'btn-crear-editorial',
        modalId: 'modalCrearEditorial',
        inputNombreId: 'nuevo-editorial-nombre',
        errorDivId: 'modalCrearEditorial-error',
        apiUrl: '/catalogo/api/crear-editorial/',
        onSuccess: function (data) {
            if (buscadorEditoriales) {
                buscadorEditoriales.agregarExterno({ id: data.id, texto: data.texto });
            }
        }
    });

    configurarModalCrear({
        btnId: 'btn-crear-productora',
        modalId: 'modalCrearProductora',
        inputNombreId: 'nuevo-productora-nombre',
        errorDivId: 'modalCrearProductora-error',
        apiUrl: '/catalogo/api/crear-productora/',
        onSuccess: function (data) {
            if (buscadorProductoras) {
                buscadorProductoras.agregarExterno({ id: data.id, texto: data.texto });
            }
        }
    });

});