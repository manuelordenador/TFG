"""
Documento base de vistas. 
"""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Usuario
from .forms import UsuarioForm


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestionUsuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            queryset = queryset.filter(nombre__icontains=busqueda)
        return queryset
    
class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = 'gestionUsuarios/usuario_detail.html'
    context_object_name = 'usuario'

class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestionUsuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

    def form_valid(self, form):
        # se puede agregar lógica antes de guardar
        return super().form_valid(form)

class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestionUsuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestionUsuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')