from django.urls import path

from .views import asignar_tecnico_views, crear_turnos_views, dias_horarios_disponibles, estado_turnos_views, modificar_estado_cron_view, vendedor_views, reprogramar_turno

from .views import visualizar_turnos_views

urlpatterns = [
    path('',visualizar_turnos_views.turnosOverview,name='turnos'),
    path('turnos-list/', visualizar_turnos_views.VisualizarTurnosViewSet.as_view({'get': 'turnosList'}), name='turnos-list'),
    path('turnos-detalle/<int:id_turno>/', visualizar_turnos_views.VisualizarTurnosViewSet.as_view({'get': 'turnoDetalle'}), name='turnos-detalle'),
    
    # -------------------------------------------------------------------------------------------------------------
    path('dias-horarios-disponibles/<int:taller_id>/', dias_horarios_disponibles.DiasHorariosDisponiblesViewSet.as_view({'get':'dias_horarios_disponibles'}), name="dias-horarios-disponibles"),
    path('dias-horarios-disponibles-turno/<int:taller_id>/<int:id_turno>/', dias_horarios_disponibles.DiasHorariosDisponiblesViewSet.as_view({'get':'dias_horarios_disponibles_turno'}), name="dias-horarios-disponibles-turno"),
    path('dias-horarios-disponibles-service/<int:taller_id>/<str:marca>/<str:modelo>/<int:km>/', dias_horarios_disponibles.DiasHorariosDisponiblesViewSet.as_view({'get':'dias_horarios_disponibles_service'}), name="dias-horarios-disponibles-service"),
    path('dias-horarios-disponibles-reparaciones/<int:taller_id>/<str:patente>/<str:origen>/', dias_horarios_disponibles.DiasHorariosDisponiblesViewSet.as_view({'get':'dias_horarios_disponibles_reparaciones'}), name="dias-horarios-disponibles-reparaciones"),
    
    path('crear-turno-evaluacion-web/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'post':'crear_turno_evaluacion_web'}), name='crear-turno-evaluacion-web'),
    path('crear-turno-evaluacion-presencial/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'post':'crear_turno_evaluacion_presencial'}), name='crear-turno-evaluacion-presencial'),
    path('crear-turno-service/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'post':'crear_turno_service'}), name='crear-turno-service'),
    path('crear-turno-reparacion/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'post':'crear_turno_reparacion'}), name='crear-turno-reparacion'),
    path('crear-turno-extraordinario/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'post':'crear_turno_extraordinario'}), name='crear-turno-extraordinario'),
    
    path('turnos-update/<int:id_turno>/', crear_turnos_views.CrearActualizarTurnosViewSet.as_view({'post':'turnoUpdate'}), name="turnos-update"),
    
    # -------------------------------------------------------------------------------------------------------------
    path('tecnicos-disponibles/<int:id_turno>/', asignar_tecnico_views.AsignarTecnicoViewSet.as_view({'get':'tecnicos_disponibles'}), name="tecnicos-disponibles"),
    path('asignar-tecnico/<int:id_tecnico>/<int:id_turno>/', asignar_tecnico_views.AsignarTecnicoViewSet.as_view({'post':'asignar_tecnico'}), name="asignar-tecnico"),
    
    # -------------------------------------------------------------------------------------------------------------
    path('pendientes/', estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_pendientes'}), name='turnos-pendientes'),
    path('en-procesos/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_en_proceso'}), name='turnos-en-procesos'),
    path('terminados/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_terminados'}), name='turnos-terminados'),
    path('cancelados/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_cancelados'}), name='turnos-cancelados'),
    path('no-validos/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'get': 'turnos_no_validos'}), name='no-validos'),
    path('actualizar-estado/<int:id_turno>/',  estado_turnos_views.EstadoTurnosViewSet.as_view({'patch': 'actualizar_estado_turno_en_proceso'}), name='actualizar-estado-turno'),
    path('cancelar-turno/<int:id_turno>/', estado_turnos_views.EstadoTurnosViewSet.as_view({'patch': 'cancelar_turno_pendiente'}), name='cancelar-turno-pendiente'),

    #--------------------------------------------------------------------------------------------------------------
    path('reprogramar-turno/', reprogramar_turno.ReprogramarTurnoViewSet.as_view({'post': 'reprogramar_turno'}), name='reprogramar-turno'),
    
    #--------------------------------------------------------------------------------------------------------------
    #path('crear-turno-vendedor/', vendedor_views.CrearTurnoVendedor.as_view({'post': 'crear_turno_vendedor'}), name='crear-turno-vendedor'),
    path('aceptar-papeles/<str:patente>/', vendedor_views.ModificarEstadosVendedor.as_view({'post': 'aceptar_papeles'}), name='aceptar-papeles'),
    path('rechazar-papeles/<str:patente>/', vendedor_views.ModificarEstadosVendedor.as_view({'post': 'rechazar_papeles'}), name='rechazar-papeles'),
    
    #--------------------------------------------------------------------------------------------------------------
    path('ejecutar-cron/', modificar_estado_cron_view.EjecutarCron.as_view({'post': 'ejecutar_cron'}), name='ejecutar-cron')
]


