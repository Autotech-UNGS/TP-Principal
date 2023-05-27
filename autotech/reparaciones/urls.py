from django.urls import path
from . import views


urlpatterns = [
    path('listar/<int:id_turno>/', views.RegistroReparacionViewSet.as_view({'get': 'listar_tareas_registro_reparacion'}), name='listar'),
    path('modificar-tarea-hechas/', views.RegistroReparacionViewSet.as_view({'patch': 'modificar_registro_tarea_hecha'}), name='modificar-tarea-hechas'),
    path('modificar-tareas-pendientes/', views.RegistroReparacionViewSet.as_view({'patch': 'modificar_registro_tarea_pendiente'}), name='modificar-tareas-pendientes'),
    path('listar-registradas/<int:id_turno>/', views.RegistroReparacionViewSet.as_view({'get': 'listar_tareas_registradas'}), name='listar-registradas'),
]
