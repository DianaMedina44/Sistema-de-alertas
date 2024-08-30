from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registroUsuario , name='registro_usuario'),
    path('inicioSesion/', views.inicioSesion, name='inicio_sesion'),
    path('crear_alerta/', views.crear_alerta, name='crear_alerta'),
    path('ver_alertas/', views.ver_alertas, name='ver_alertas'),
    path('cerrarSesion/', views.cerrarSesion, name='cerrar_sesion'),
    path('alerta/<int:pk>/', views.alerta_detalle, name='alerta_detalle')

    
]