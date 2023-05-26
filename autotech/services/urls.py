from django.urls import path
from .views.visualizar_service import *
from .views.alta_service import *
from .views.alta_checklist_service import *


urlpatterns = [
    path('listar/', VisualizarServiceList.as_view(), name = 'visualizar-services'),
    path('listar-uno/<int:id_service>/', VisualizarServiceUno.as_view(), name = 'visualizar-services-uno'),
    path('crear/', ServiceCreate.as_view(), name ='crear-services'),  
]
