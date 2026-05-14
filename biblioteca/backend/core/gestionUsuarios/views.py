"""
Documento base de vistas. 
"""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm


class UsuarioListView(ListView):
    model = Usuario
    template_name = 'gestionUsuarios/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = Usuario.objects.all()
        busqueda = self.request.GET.get('busqueda')
        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) |
                Q(apellidos__icontains=busqueda) |
                Q(correo_e__icontains=busqueda)
                )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = Usuario.objects.count()
        context['titulo'] = 'Lista de Usuarios'
        return context
    
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
        messages.success(self.request, f'Usuario {form.instance.nombre} {form.instance.apellidos} creado exitosamente')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corrige los errores en el formulario')
        return super().form_invalid(form)


class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'gestionUsuarios/usuario_form.html'
    success_url = reverse_lazy('usuario_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # En edición, no requerimos confirmar contraseña si no se cambia
        if 'passwordConfirm' in form.fields:
            form.fields['passwordConfirm'].required = False
        return form
    
    def form_valid(self, form):
        messages.success(self.request, f'Usuario {form.instance.nombre} {form.instance.apellidos} actualizado')
        return super().form_valid(form)

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'gestionUsuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')

    def delete(self, request, *args, **kwargs):
        usuario = self.get_object()
        messages.success(request, f'Usuario {usuario.nombre} {usuario.apellidos} eliminado')
        return super().delete(request, *args, **kwargs)