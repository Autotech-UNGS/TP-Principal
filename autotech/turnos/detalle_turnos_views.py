import requests
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.models import Turno_taller
from tecnicos.consumidor_api_externa import ConsumidorApiTecnicos
from .validaciones_views import ValidadorSupervisor


class DetalleTurnosViewSet(ViewSet):
    validador_sup = ValidadorSupervisor()

    @action(detail=True, methods=['get'])
    def detalle_turno(self, request, id_turno):
        try:
            turno= Turno_taller.objects.get(id_turno=id_turno)
        except Turno_taller.DoesNotExist:
            return HttpResponse('error: el turno no existe', status=400) 
        try:
            if turno.estado == 'pendiente':
                turno_data = self.obtener_data_turno_pendiente(turno)
            else:
                turno_data = self.obtener_data_turno_en_proceso_terminado(turno)
            return Response(turno_data)
        except requests.HTTPError as e:
            return HttpResponse(str(e), status=e.response.status_code)
        except Exception as e:
                return HttpResponse('error: el id ingresado no corresponde a un tecnico', status=404)
 
    def obtener_data_turno_pendiente(self, turno):
        turno_data = {
                    'id_turno': turno.id_turno,
                    'patente': turno.patente,
                    'estado': turno.estado,
                    'tipo': turno.tipo,
                    'fecha_inicio': turno.fecha_inicio,
                    'hora_inicio': turno.hora_inicio,
                    'fecha_fin': turno.fecha_fin,
                    'hora_fin': turno.hora_fin,
                    'papeles_en_regla': turno.papeles_en_regla
        }
        if(turno.tipo == 'service'):
            turno_data['frecuencia_km'] = turno.frecuencia_km  
        return turno_data

    def obtener_data_turno_en_proceso_terminado(self, turno):
        nombre_tecnico = ConsumidorApiTecnicos.obtener_nombre_tecnico(turno.tecnico_id)
        categoria_tecnico = ConsumidorApiTecnicos.obtener_categoria_tecnico(turno.tecnico_id)
        estado = turno.estado
        if estado == 'en_proceso':
            estado = 'en proceso'
        turno_data = {
                    'id_turno': turno.id_turno,
                    'patente': turno.patente,
                    'estado': estado,
                    'tipo': turno.tipo,
                    'fecha_inicio': turno.fecha_inicio,
                    'hora_inicio': turno.hora_inicio,
                    'fecha_fin': turno.fecha_fin,
                    'hora_fin': turno.hora_fin,
                    'tecnico_id': turno.tecnico_id,
                    'nombre_completo': nombre_tecnico,
                    'categoria': categoria_tecnico,
                }
        if turno.tipo == 'service':
            turno_data['frecuencia_km'] = turno.frecuencia_km     
        return turno_data
  
    def obtener_data_turnos_pendientes(self, turnos):
        turnos_data = []
        for turno in turnos:
            turno_data = {
                'id_turno': turno.id_turno,
                'patente': turno.patente,
                'estado': turno.estado,
                'tipo': turno.tipo,
                'fecha_inicio': turno.fecha_inicio,
                'hora_inicio': turno.hora_inicio,
            }
            turnos_data.append(turno_data)
        return turnos_data

    def obtener_data_turnos_en_proceso_terminado(self, turnos, estado):
        turnos_data = []
        for turno in turnos:
            nombre_tecnico = ConsumidorApiTecnicos.obtener_nombre_tecnico(turno.tecnico_id)
            #import pdb; pdb.set_trace()
            estado = turno.estado
            if estado == 'en_proceso':            
                turno_data = {
                    'id_turno': turno.id_turno,
                    'patente': turno.patente,
                    'estado': 'en proceso',
                    'tipo': turno.tipo,
                    'fecha_inicio': turno.fecha_inicio,
                    'hora_inicio': turno.hora_inicio,
                    'tecnico_id': turno.tecnico_id,
                    'nombre_completo': nombre_tecnico,
                }
            else:
                turno_data = {
                    'id_turno': turno.id_turno,
                    'patente': turno.patente,
                    'estado': turno.estado,
                    'tipo': turno.tipo,
                    'fecha_inicio': turno.fecha_inicio,
                    'hora_inicio': turno.hora_inicio,
                    'fecha_fin': turno.fecha_fin,
                    'hora_fin': turno.hora_fin,
                    'tecnico_id': turno.tecnico_id,
                    'nombre_completo': nombre_tecnico,          
                }
            turnos_data.append(turno_data)
        return turnos_data
            