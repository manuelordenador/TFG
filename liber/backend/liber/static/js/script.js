document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("toggle-theme");
    if (!btn) {
        console.error("Botón 'toggle-theme' no encontrado");
        return;
    }
    const html = document.documentElement;

    const temaGuardado = localStorage.getItem("tema");


    if (temaGuardado) {
        html.setAttribute("data-bs-theme", temaGuardado);
    }

    btn.addEventListener("click", function () {
        const current = html.getAttribute("data-bs-theme");
        const next = current === "dark" ? "light" : "dark";
        html.setAttribute("data-bs-theme", next);
        localStorage.setItem("tema", next);
    });
    
});