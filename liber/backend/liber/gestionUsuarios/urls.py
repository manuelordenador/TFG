from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .decorators import solo_invitados
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
    path('<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
]
