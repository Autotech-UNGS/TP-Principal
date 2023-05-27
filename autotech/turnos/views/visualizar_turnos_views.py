from django.http import JsonResponse, HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..enviar_turno_email import EnvioDeEmail
from ..obtener_datos import *
from ..validaciones_views import * 
from datetime import *
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

@api_view(['GET'])
def turnosOverview(request):
    turnos_urls={
        'List':'turnos-list/',
        'Detalle':'turnos-detalle/<str:id_turno>/',
        'Create':'turnos-create/',
        'Update':'turnos-update/<int:id_turno>/',
        'DiasHorariosDisponibles':'dias-horarios-disponibles/<str:taller_id>',        
        'Tecnicos-disponibles':'tecnicos-disponibles/<int:id_turno>/',
        'Asignar-tecnico':'asignar-tecnico/<int:id_tecnico>/<int:_id_turno>/',
        'Turnos-pendientes': 'pendientes/',
        'Turnos-en-proceso': 'en-procesos/',
        'Turnos-terminados': 'terminados/',
        'Finalizar-turno': 'actualizar-estado/<int:id_turno>/',
        'cancelar-turno': 'cancelar-turno/<int:id_turno>/'
    }
    return Response(turnos_urls)

class VisualizarTurnosViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def turnosList(self, request):
        turnos= Turno_taller.objects.all()
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def turnoDetalle(self, request, id_turno):
        try:
            turno=Turno_taller.objects.get(id_turno=id_turno)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        else:
            serializer= TurnoTallerSerializer(turno,many=False)
            return Response(serializer.data)
