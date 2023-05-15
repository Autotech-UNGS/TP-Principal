from django.urls import path

from . import views
from . import estado_turnos

urlpatterns = [
    path('',views.turnosOverview,name='turnos'),

    path('turnos-list/', views.turnosList, name='turnos-list'),

    path('turnos-detalle/<int:id_turno>/', views.turnoDetalle, name='turnos-detalle'),

    path('turnos-create/', views.crearTurno,name="turnos-create"),

    path('turnos-update/<int:id_turno>/', views.turnoUpdate,name="turnos-update"),
    
    path('dias-horarios-disponibles/<int:taller_id>/', views.diasHorariosDisponibles,name="dias-horarios-disponibles"),

    # -------------------------------------------------------------------------------------------------------------
    path('pendientes/', estado_turnos.EstadoTurnosViewSet.as_view({'get': 'turnos_pendientes'}), name='turnos-pendientes'),
    path('en_proceso/',  estado_turnos.EstadoTurnosViewSet.as_view({'get': 'turnos_en_proceso'}), name='turnos-en-proceso'),
    path('terminados/',  estado_turnos.EstadoTurnosViewSet.as_view({'get': 'turnos_terminados'}), name='turnos-terminados'),
    path('actualizar_estado/<int:pk>/',  estado_turnos.EstadoTurnosViewSet.as_view({'patch': 'actualizar_estado_turno_en_proceso'}), name='actualizar-estado-turno')
]


