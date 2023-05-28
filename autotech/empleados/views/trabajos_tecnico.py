import requests
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.serializers import TurnoTallerSerializer
from administracion.models import Turno_taller
from .validadores_views import ValidadorDatosEmpleado


class TrabajosTecnicoViewSet(ViewSet):
    @action(detail=True, methods=['get'])
    def detalle_trabajos_tecnico(self, request, id_tecnico):
        validador_sup = ValidadorDatosEmpleado()
        taller_sup= request.GET.get('branch')       
        
        if not validador_sup.taller(taller_sup):
            return HttpResponse('error: numero de taller no valido', status=400)      
        
        id_taller = int(taller_sup[-3:])
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, taller_id=id_taller).order_by('estado')
        data = []
        
        for turno in turnos:
            data.append({
                "id_turno": turno.id_turno,
                "patente": turno.patente,
                "fecha_inicio": turno.fecha_inicio,
                "hora_inicio": turno.hora_inicio,
                "fecha_fin": turno.fecha_fin,
                "hora_fin": turno.hora_fin,
                "tipo": turno.tipo,
                "estado": turno.estado
            })
        
        return Response(data)

    @action(detail=True, methods=['get'])
    def trabajos_en_proceso_tecnico(self, request, id_tecnico):
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso')
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])   
    def trabajos_terminados_tecnico(self, request, id_tecnico):
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='terminado')
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)
    # -------------------------------------------------------------------------------------------------------
    @action(detail=True, methods=['get'])   
    def trabajos_en_proceso_evaluacion_tecnico(self, request, id_tecnico):
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='evaluacion')
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])   
    def trabajos_en_proceso_service_tecnico(self, request, id_tecnico):
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='service')
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])   
    def trabajos_en_proceso_reparacion_tecnico(self, request, id_tecnico):
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='reparacion')
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])   
    def trabajos_en_proceso_extraordinario_tecnico(self, request, id_tecnico):
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='extraordinario')
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)
    
    # -------------------------------------------------------------------------------------------------------