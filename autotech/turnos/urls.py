from django.urls import path

from . import estado_turnos_views, detalle_turnos_views, modificar_estado_cron_view, visualizar_turnos_views, crear_turnos_views, asignar_tecnico_views

urlpatterns = [
    path('',visualizar_turnos_views.turnosOverview,name='turnos'),
    path('turnos-list/', visualizar_turnos_views.VisualizarTurnosViewSet.as_view({'get': 'turnosList'}), name='turnos-list'),
    path('turnos-detalle/<int:id_turno>/', visualizar_turnos_views.VisualizarTurnosViewSet.as_view({'get': 'turnoDetalle'}), name='turnos-detalle'),
    
    # -------------------------------------------------------------------------------------------------------------
    path('turnos-create/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'post':'crearTurno'}), name="turnos-create"),
    path('turnos-update/<int:id_turno>/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'post':'turnoUpdate'}), name="turnos-update"),
    path('dias-horarios-disponibles/<int:taller_id>/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'get':'diasHorariosDisponibles'}), name="dias-horarios-disponibles"),    
    
    # -------------------------------------------------------------------------------------------------------------
    path('tecnicos-disponibles/<int:id_turno>/', asignar_tecnico_views.AsignarTecnicoViewSet.as_view({'get':'tecnicos_disponibles'}), name="tecnicos-disponibles"),
    path('asignar-tecnico/<int:id_tecnico>/<int:id_turno>/', asignar_tecnico_views.AsignarTecnicoViewSet.as_view({'post':'asignar_tecnico'}), name="asignar-tecnico"),
    
    # -------------------------------------------------------------------------------------------------------------
    path('pendientes/', estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_pendientes'}), name='turnos-pendientes'),
    path('en-procesos/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_en_proceso'}), name='turnos-en-procesos'),
    path('terminados/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_terminados'}), name='turnos-terminados'),
    path('actualizar-estado/<int:id_turno>/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'patch': 'actualizar_estado_turno_en_proceso'}), name='actualizar-estado-turno'),
    path('cancelar-turno/<int:id_turno>/', estado_turnos_views.EstadoTurnosViewSet.as_view({'patch': 'cancelar_turno_pendiente'}), name='cancelar-turno-pendiente'),

    #--------------------------------------------------------------------------------------------------------------
    path('detalle-turno/<int:id_turno>/', detalle_turnos_views.DetalleTurnosViewSet.as_view({'get': 'detalle_turno'}), name='detalle-turno'),
    
    #--------------------------------------------------------------------------------------------------------------
    path('ejecutar-cron/', modificar_estado_cron_view.EjecutarCron.as_view({'get': 'ejecutar_cron'}), name='ejecutar_cron')
]


