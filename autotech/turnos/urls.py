from django.urls import path

from . import views, estado_turnos_views, detalle_turnos_views

urlpatterns = [
    path('',views.turnosOverview,name='turnos'),

    path('turnos-list/', views.turnosList, name='turnos-list'),

    path('turnos-detalle/<int:id_turno>/', views.turnoDetalle, name='turnos-detalle'),

    path('turnos-create/', views.crearTurno,name="turnos-create"),

    path('turnos-update/<int:id_turno>/', views.turnoUpdate,name="turnos-update"),
    
    path('dias-horarios-disponibles/<int:taller_id>/', views.diasHorariosDisponibles,name="dias-horarios-disponibles"),

    # -------------------------------------------------------------------------------------------------------------
    path('pendientes/', estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_pendientes'}), name='turnos-pendientes'),
    path('en-proceso/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_en_proceso'}), name='turnos-en-proceso'),
    path('terminados/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_terminados'}), name='turnos-terminados'),
    path('actualizar-estado/<int:id_turno>/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'patch': 'actualizar_estado_turno_en_proceso'}), name='actualizar-estado-turno'),
    path('cancelar-turno/<int:id_turno>/', estado_turnos_views.EstadoTurnosViewSet.as_view({'patch': 'cancelar_turno_pendiente'}), name='cancelar-turno-pendiente'),

    #--------------------------------------------------------------------------------------------------------------
    path('detalle-turno/<int:id_turno>/', detalle_turnos_views.DetalleTurnosViewSet.as_view({'get': 'detalle_turno'}), name='detalle-turno')
]


