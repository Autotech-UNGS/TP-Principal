from django.urls import path
from .views.visualizar_service import *


urlpatterns = [
    path('listar/', VisualizarServiceList.as_view(),name = 'visualizar-services')

]
