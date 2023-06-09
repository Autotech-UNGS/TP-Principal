from django.urls import path
from .views import *
from .visualizar_evaluacion_admin import RegistroEvaluacionAdminViewSet

urlpatterns = [
    path('registros/crear/', RegistroEvaluacionCreate.as_view(), name= 'crear_registro_evaluacion'),

    path('registros/listar/', RegistroEvaluacionList.as_view(), name='listar_registro_evaluacion'),
    path('registros/listar/<int:id_tecnico>/', RegistroEvaluacionListTecnico.as_view(), name='listar_registro_evaluacion_tecnico'),

    path('registros/listar/detalle/',RegistroEvaluacionXAdminReadOnly.as_view(), name='listar_registro_evaluacion_admin'),
    
    path('registros/listar/detalle/<int:id_tecnico>/', RegistroEvaluacionXAdminReadOnlyTecnico.as_view(), name='listar_registro_evaluacion_admin_tecnico'), 

    #path('registros/listar/<int:id_turno>/', RegistroEvaluacionUno.as_view(), name = 'listar_registros_evaluacion_por_id'),

    path('checklist/listar/', ChecklistEvaluacionList.as_view(), name= 'listar_checklist_evaluacion'),

    path('registro-extraordinario/crear/', RegistroExtraordinarioCreate.as_view(), name= 'crear_registro_extraordinario'),
    path('registros-extraordinario/listar/<int:id_tecnico>/', RegistroExtraordinarioListTecnico.as_view(), name= 'listar_registro_extraordinario'),

    # -------------------------------------- PARA ADMIN ----------------------------------------------- #
    path('registros/',RegistroEvaluacionAdminViewSet.as_view(actions={'get': 'list'}), name = 'admin-evaluaciones'),
    path('registro/patente/<str:patente>/',RegistroEvaluacionAdminViewSet.as_view(actions={'get': 'obtener_ultimo_registro_patente'}), name = 'registros-x-patente-evaluaciones'),

    
]


