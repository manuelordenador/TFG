"""
Documento base de vistas de la gestión de usuarios.s
"""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario
from .forms import *


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'gestionUsuarios/registro.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'gestionUsuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def perfil_view(request):
    return render(request, 'gestionUsuarios/perfil.html')

# class UsuarioListView(ListView):
#     model = Usuario
#     template_name = 'gestionUsuarios/usuario_list.html'
#     context_object_name = 'usuarios'
#     paginate_by = 10

#     def get_paginate_by(self, queryset):
#         return self.request.GET.get('por_pagina', 10)

#     def get_queryset(self):
#         queryset = Usuario.objects.all()
#         busqueda = self.request.GET.get('busqueda')
#         if busqueda:
#             queryset = queryset.filter(
#                 Q(nombre__icontains=busqueda) |
#                 Q(apellidos__icontains=busqueda) |
#                 Q(correo_e__icontains=busqueda)
#                 )
#         return queryset
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total_usuarios'] = Usuario.objects.count()
#         context['titulo'] = 'Lista de Usuarios'
#         return context

# class UsuarioDetailView(DetailView):
#     model = Usuario
#     template_name = 'gestionUsuarios/usuario_detail.html'
#     context_object_name = 'usuario'

# class UsuarioCreateView(CreateView):
#     model = Usuario
#     form_class = UsuarioForm
#     template_name = 'gestionUsuarios/usuario_form.html'
#     success_url = reverse_lazy('usuario_list')

#     def form_valid(self, form):
#         messages.success(self.request, f'Usuario {form.instance.nombre} {form.instance.apellidos} creado exitosamente')
#         return super().form_valid(form)
    
#     def form_invalid(self, form):
#         messages.error(self.request, 'Por favor corrige los errores en el formulario')
#         return super().form_invalid(form)

# class UsuarioUpdateView(UpdateView):
#     model = Usuario
#     form_class = UsuarioForm
#     template_name = 'gestionUsuarios/usuario_form.html'
#     success_url = reverse_lazy('usuario_list')

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         # En edición, no requerimos confirmar contraseña si no se cambia
#         if 'passwordConfirm' in form.fields:
#             form.fields['passwordConfirm'].required = False
#         return form
    
#     def form_valid(self, form):
#         messages.success(self.request, f'Usuario {form.instance.nombre} {form.instance.apellidos} actualizado')
#         return super().form_valid(form)

# class UsuarioDeleteView(DeleteView):
    # model = Usuario
    # template_name = 'gestionUsuarios/usuario_confirm_delete.html'
    # success_url = reverse_lazy('usuario_list')

    # # método que borra al usuario de la bdd
    # def delete(self, request, *args, **kwargs):
    #     usuario = self.get_object()
    #     messages.success(request, f'Usuario {usuario.nombre} {usuario.apellidos} eliminado')
    #     return super().delete(request, *args, **kwargs) #llamada al método de borrado de la calse django deleteView