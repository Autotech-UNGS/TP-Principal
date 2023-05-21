from django.urls import path, reverse, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rest_framework.views import APIView

from .views import *

urlpatterns = [
    path('registros/crear/', RegistroEvaluacionCreate.as_view(), name= 'crear_registro_evaluacion'),

    path('registros/listar/', RegistroEvaluacionList.as_view(), name='listar_registro_evaluacion'),
    path('registros/listar/<int:id_tecnico>/', RegistroEvaluacionListTecnico.as_view(), name='listar_registro_evaluacion_tecnico'),

    path('registros/listar/detalle/',RegistroEvaluacionXAdminReadOnly.as_view(), name='listar_registro_evaluacion_admin'),
    
    path('registros/listar/detalle/<int:id_tecnico>/', RegistroEvaluacionXAdminReadOnlyTecnico.as_view(), name='listar_registro_evaluacion_admin_tecnico'), 

    #path('registros/listar/<int:id_turno>/', RegistroEvaluacionUno.as_view(), name = 'listar_registros_evaluacion_por_id'),

    path('checklist/listar/', ChecklistEvaluacionList.as_view(), name= 'listar_checklist_evaluacion')

    
]


