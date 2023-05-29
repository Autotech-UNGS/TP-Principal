from django.http import JsonResponse, HttpResponse
from administracion.models import *
from ..obtener_datos import *
from datetime import *
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from django.core import serializers
from django.http import JsonResponse
from ..validaciones_crear_turno import validaciones

class ReprogramarTurnoViewSet(ViewSet):
    @action(detail=False, methods=['post'])
    def reprogramar_turno(self, request):
        """
        id_turno
        fecha_inicio
        hora_inicio
        """
        nueva_fecha_inicio = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        nueva_hora_inicio = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        id_turno = request.data.get("id_turno")
        
        # datos del turno necesarios para validaciones
        turno = obtener_turno(id_turno)
        if turno == None:
            return HttpResponse("error: no hay un turno con la id solicitada.", status=400)
        taller_id = str(turno.taller_id.id_taller)
        vieja_fecha_inicio = turno.fecha_inicio
        vieja_hora_inicio = turno.hora_inicio
        vieja_fecha_fin = turno.fecha_fin
        vieja_hora_fin = turno.hora_fin
        patente = turno.patente
        tipo = turno.tipo
        
        duracion = obtener_duracion(vieja_fecha_inicio, vieja_hora_inicio, vieja_fecha_fin, vieja_hora_fin)
        nueva_fecha_hora_fin = obtener_fecha_hora_fin(nueva_fecha_inicio, nueva_hora_inicio, duracion)
        
        if turno.estado != 'cancelado':
            return HttpResponse("error: el turno debe estar cancelado para poder reprogramarse.", status=400)
        resultado_validacion = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo=tipo, 
                                                                   dia_inicio=nueva_fecha_inicio, horario_inicio=nueva_hora_inicio,
                                                                   dia_fin= nueva_fecha_hora_fin[0], horario_fin=nueva_fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        
        # datos para crear el nuevo turno:
        estado = 'pendiente'
        patente = turno.patente
        frecuencia_km = turno.frecuencia_km
        papeles_en_regla = turno.papeles_en_regla
        
        nuevo_turno = Turno_taller.objects.create(tipo= tipo, estado= estado, taller_id = turno.taller_id, patente=patente, 
                                                  fecha_inicio=nueva_fecha_inicio, hora_inicio= nueva_hora_inicio, 
                                                  fecha_fin= nueva_fecha_hora_fin[0], hora_fin=nueva_fecha_hora_fin[1], 
                                                  frecuencia_km= frecuencia_km, papeles_en_regla= papeles_en_regla)
        
        nuevo_turno_data = serializers.serialize('json', [nuevo_turno])
        nuevo_turno_data = json.loads(nuevo_turno_data)[0]['fields']
        nuevo_turno_data['id_turno'] = nuevo_turno.id_turno
        nuevo_turno_data['tipo'] = nuevo_turno.tipo
        nuevo_turno_data['estado'] = nuevo_turno.estado
        nuevo_turno_data['taller_id'] = nuevo_turno.taller_id.id_taller
        nuevo_turno_data['tecnico_id'] = nuevo_turno.tecnico_id
        nuevo_turno_data['patente'] = nuevo_turno.patente
        nuevo_turno_data['fecha_inicio'] = nuevo_turno.fecha_inicio
        nuevo_turno_data['hora_inicio'] = nuevo_turno.hora_inicio
        nuevo_turno_data['fecha_fin'] = nuevo_turno.fecha_fin
        nuevo_turno_data['hora_fin'] = nuevo_turno.hora_fin
        nuevo_turno_data['frecuencia_km'] = nuevo_turno.frecuencia_km
        nuevo_turno_data['papeles_en_regla'] = nuevo_turno.papeles_en_regla
        
        return JsonResponse(nuevo_turno_data, json_dumps_params={'indent': 4})