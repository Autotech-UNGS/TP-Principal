from django.urls import path
from .views.visualizar_service import *
from .views.alta_service import *
from .views.alta_checklist_service import *
from .views.cambiar_estado_service import *
from .views.visualizar_service_admin import RegistroServiceAdminViewSet


urlpatterns = [
    path('listar/', VisualizarServiceList.as_view(), name = 'visualizar-services'),
    path('listar/<int:id_service>/', VisualizarServiceUno.as_view(), name = 'visualizar-services-uno'),
    path('crear/', ServiceCreate.as_view(), name ='crear-services'),  
    path('actualizar-estado/<int:id_service>/',ActualizarEstado.as_view(), name = 'actualizar-estado-service'),
    path('listar/checklist/',ChecklistEvaluacionListar.as_view(), name = 'visualizar-checklist'),
    path('listar/checklist/<int:id_service>/', VisualizarTareasService.as_view(), name='visualizar-tarea-service'),
    path('listar/registros-pendientes/<int:id_tecnico>/', ListarTurnosRegistroPendienteTecnico.as_view(), name='visualizar-registros-service-pendientes'),

     # -------------------------------------- PARA ADMIN ----------------------------------------------- #
    path('registros/',RegistroServiceAdminViewSet.as_view(actions={'get': 'list'}), name = 'admin-service'),
    path('registro/patente/<str:patente>/',RegistroServiceAdminViewSet.as_view(actions={'get': 'obtener_ultimo_registro_patente'}), name = 'registros-x-patente-service'),
]
