from django.http import HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from ..gestion_garantia import GestionGarantias
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from datetime import date
from turnos.obtener_datos import *

"""
class VerificarEstadoGarantia(ViewSet):    
    @action(detail=True, methods=['get'])
    def mantiene_garantia(self, request, patente:str, fecha_turno:date, service_actual:int):
        patente = patente.upper()
        ultimo_service = obtener_frecuencia_ultimo_service(patente)
        mantiene_garantia = GestionGarantias.garantia_vigente()
"""