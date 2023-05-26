from django.urls import path
from .views.visualizar_service import *
from .views.alta_service import *
from .views.alta_checklist_service import *
from .views.cambiar_estado_service import *


urlpatterns = [
    path('listar/', VisualizarServiceList.as_view(), name = 'visualizar-services'),
    path('listar/<int:id_service>/', VisualizarServiceUno.as_view(), name = 'visualizar-services-uno'),
    path('crear/', ServiceCreate.as_view(), name ='crear-services'),  
    path('actualizar-estado/<int:id_service>/',ActualizarEstado.as_view(), name = 'actualizar-estado-service'),
    path('listar/checklist/',ChecklistEvaluacionListar.as_view(), name = 'visualizar-checklist'),
    path('listar/checklist/<int:id_service>/', VisualizarTareasService.as_view(), name='visualizar-tarea-service'),
]
