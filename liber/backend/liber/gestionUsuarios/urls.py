from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .decorators import solo_invitados

app_name = 'gestionUsuarios'

urlpatterns = [
    # lógica de inicio de sesión
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    
    # Recuperación de contraseñas
    path("reset-password/", solo_invitados(auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt',
        success_url='/usuarios/reset-password-sent/',
        )), name="reset_password"),
    path("reset-password-sent/", solo_invitados(auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html')), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", solo_invitados(auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html',
        success_url='/usuarios/reset-password-complete/',
        )), name="password_reset_confirm"),
    path("reset-password-complete/", solo_invitados(auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html')), name="password_reset_complete"),

    # lógica de visionado y edición de datos
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('alta_socio/', views.alta_socio_view, name='alta_socio'),
    path('crear_bibliotecario/', views.crear_bibliotecario_view, name='crear_bibliotecario'),
    path('<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('configuracion_cuenta', views.configuracion_cuenta, name='configuracion_cuenta'),
    path(
        'cambiar-contraseña/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change_form.html',
            success_url=reverse_lazy('password_change_done'),
        ),
        name='password_change',
    ),
    path(
        'cambiar-contraseña/hecho/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html',
        ),
        name='password_change_done',
    ),
]
