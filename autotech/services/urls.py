from django.urls import path
from .views import alta_service, alta_checklist_service , cambiar_estado_service, visualizar_service_admin, visualizar_service, registro_info_service


urlpatterns = [
    path('crear/', alta_service.ServiceCreate.as_view(), name ='crear-services'),  
    
    path('listar/', visualizar_service.VisualizarServiceList.as_view(), name = 'visualizar-services'),
    path('listar/<int:id_service>/', visualizar_service.VisualizarServiceUno.as_view(), name = 'visualizar-services-uno'),
    
    path('actualizar-estado/<int:id_service>/',cambiar_estado_service.ActualizarEstado.as_view(), name = 'actualizar-estado-service'),

    path('listar/checklist/',alta_checklist_service.ChecklistEvaluacionListar.as_view(), name = 'visualizar-checklist'),
    path('listar/checklist-service/<int:id_service>/', visualizar_service.VisualizarTareasService.as_view(), name='visualizar-tareas-service'),
    path('listar/checklist-turno/<int:id_turno>/', visualizar_service.VisualizarTareasServicePorTurno.as_view(), name='visualizar-tareas-service-turno'),

    path('precio/', visualizar_service.VisualizarPrecioService.as_view(), name ='visualizar-precio-service'),

    path('crear/registro/', registro_info_service.RegistroServiceCreate.as_view(), name ='crear-registro-service'),
    path('listar/registros-pendientes/<int:id_tecnico>/', registro_info_service.ListarTurnosRegistroPendienteTecnico.as_view(), name='visualizar-registros-service-pendientes'),



     # -------------------------------------- PARA ADMIN ----------------------------------------------- #
    path('registros/',visualizar_service_admin.RegistroServiceAdminViewSet.as_view(actions={'get': 'list'}), name = 'admin-service'),
    path('registro/patente/<str:patente>/',visualizar_service_admin.RegistroServiceAdminViewSet.as_view(actions={'get': 'obtener_ultimo_registro_patente'}), name = 'registros-x-patente-service'),
]
