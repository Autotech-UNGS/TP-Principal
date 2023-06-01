from django.urls import path
from . import views


urlpatterns = [
    path('listar/<int:id_turno>/', views.RegistroReparacionViewSet.as_view({'get': 'listar_tareas_registro_reparacion'}), name='listar'),
    path('modificar-tareas-hechas/', views.RegistroReparacionViewSet.as_view({'patch': 'modificar_registro_tarea_hecha'}), name='modificar-tareas-hechas'),
    path('modificar-tareas-pendientes/', views.RegistroReparacionViewSet.as_view({'patch': 'modificar_registro_tarea_pendiente'}), name='modificar-tareas-pendientes'),
    path('listar-registradas/<int:id_turno>/', views.RegistroReparacionViewSet.as_view({'get': 'listar_tareas_registradas'}), name='listar-registradas'),
    path('ver-detalle-evaluacion/<int:id_turno>/', views.RegistroReparacionViewSet.as_view({'get': 'mostrar_detalle_evaluacion_realizada'}), name='mostrar-detalle-evaluacion'),
    path('modificar-detalle-reparacion/', views.RegistroReparacionViewSet.as_view({'patch': 'modificar_detalle_reparacion'}), name='mostrar-detalle-evaluacion'),
    path('listar-en-proceso/<int:id_tecnico>/', views.RegistroReparacionViewSet.as_view({'get': 'listar_turnos_registro_en_proceso'}), name='listar-en-proceso'),
    path('finalizar/<int:id_turno>/', views.RegistroReparacionViewSet.as_view({'patch': 'finalizar_registro'}), name='finalizar-registro'),
]
