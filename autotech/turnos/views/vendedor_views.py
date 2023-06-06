from django.http import HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from ..obtener_datos import *
from ..validaciones_asignar_tecnico import * 
from datetime import *
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
    
class ModificarEstadosVendedor(ViewSet):    
    # el estado de los papeles del turno pasa a ser True
    @action(detail=True, methods=['post'])
    def aceptar_papeles(self, request, patente):
        try:
            turno = Turno_taller.objects.get(patente= patente)
        except:
            return HttpResponse("error: la patente ingresada no pertenece a ningún turno en el sistema", status=400)
        else:
            if turno.tipo != 'evaluacion':
                return HttpResponse("error: la patente ingresada pertenece a un vehículo sin turno para evaluación", status=400)
            if turno.estado == 'rechazado':
                return HttpResponse("error: la patente ingresada pertenece a un vehículo cuyos papeles ya fueron rechazados", status=400)
            elif turno.estado != 'pendiente':
                return HttpResponse(f"error: la patente ingresada pertenece a un vehículo con estado {turno.estado}", status=400)
            
            turno.papeles_en_regla = True
            turno.save()
            serializer= TurnoTallerSerializer(turno,many=False) # retornamos el turno, donde debería verse el estado de los papeles True
            return Response(serializer.data)
    
    # el estado del turno pasa a ser rechazado
    @action(detail=True, methods=['post'])
    def rechazar_papeles(self, request, patente):
        try:
            turno = Turno_taller.objects.get(patente= patente)
        except:
            return HttpResponse("error: la patente ingresada no pertenece a ningún turno en el sistema", status=400)
        else:
            if turno.tipo != 'evaluacion':
                return HttpResponse("error: la patente ingresada pertenece a un vehículo sin turno para evaluación", status=400)
            if turno.estado != 'pendiente':
                return HttpResponse(f"error: la patente ingresada pertenece a un vehículo con estado {turno.estado}", status=400)
            
            turno.papeles_en_regla = False
            turno.save()
            turno.estado = 'rechazado'
            turno.save()
            serializer= TurnoTallerSerializer(turno,many=False) # retornamos el turno, donde debería verse el estado del turno rechazado
            return Response(serializer.data)
    