from django.http import JsonResponse, HttpResponse
from administracion.models import *
from ..obtener_datos import *
from ..validaciones_views import * 
from datetime import *
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from django.core import serializers
from django.http import JsonResponse

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
        turno = self.obtener_turno(id_turno)
        if turno == None:
            return HttpResponse("error: no hay un turno con la id solicitada.", status=400)
        taller_id = turno.taller_id.id_taller
        vieja_fecha_inicio = turno.fecha_inicio
        vieja_hora_inicio = turno.hora_inicio
        vieja_fecha_fin = turno.fecha_fin
        vieja_hora_fin = turno.hora_fin
        
        duracion = obtener_duracion(vieja_fecha_inicio, vieja_hora_inicio, vieja_fecha_fin, vieja_hora_fin)
        nueva_fecha_hora_fin = obtener_fecha_hora_fin(nueva_fecha_inicio, nueva_hora_inicio, duracion)
        
        if turno.estado != 'cancelado':
            return HttpResponse("error: el turno debe estar cancelado para poder reprogramarse.", status=400)
        taller_valido = self.validar_taller(taller_id= taller_id, dia_inicio=nueva_fecha_inicio, horario_inicio= nueva_hora_inicio, dia_fin= nueva_fecha_hora_fin[0], horario_fin=nueva_fecha_hora_fin[1])
        if taller_valido.status_code == 400:
            return taller_valido
        dias_horarios_validos = self.validar_dias_horarios(dia_inicio=nueva_fecha_inicio, horario_inicio= nueva_hora_inicio, dia_fin= nueva_fecha_hora_fin[0], horario_fin=nueva_fecha_hora_fin[1])
        if dias_horarios_validos.status_code == 400:
            return dias_horarios_validos
        
        # datos para crear el nuevo turno:
        tipo = turno.tipo
        estado = 'pendiente'
        patente = turno.patente
        frecuencia_km = turno.frecuencia_km
        papeles_en_regla = turno.papeles_en_regla
        
        nuevo_turno = Turno_taller.objects.create(tipo= tipo, estado= estado, taller_id = taller_id, patente=patente, 
                                                  fecha_inicio=nueva_fecha_inicio, hora_inicio= nueva_hora_inicio, 
                                                  fecha_fin= nueva_fecha_hora_fin[0], hora_fin=nueva_fecha_hora_fin[1], 
                                                  frecuencia_km= frecuencia_km, papeles_en_regla= papeles_en_regla)
        nuevo_turno_json = serializers.serialize('json', [nuevo_turno])
        return JsonResponse(nuevo_turno_json, safe=False)
        
# ---------------------------------------------------------------------------------------- #
# ------------------------------------- validaciones ------------------------------------- #
# ---------------------------------------------------------------------------------------- #
    def obtener_turno(self, id_turno:int) -> Turno_taller:
        try:
            turno = Turno_taller.objects.get(id_turno = id_turno)
            return turno
        except:
            return None

    def validar_taller(self, taller_id:str, dia_inicio:date, horario_inicio:time, dia_fin:date, horario_fin:time) -> HttpResponse:
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)
        if not taller_esta_disponible(taller_id, dia_inicio, horario_inicio, dia_fin, horario_fin):
            return HttpResponse("error: ese dia no esta disponible en ese horario", status=400)
        return HttpResponse("Taller correcto", status=200)
        
    def validar_dias_horarios(self, dia_inicio:date, horario_inicio:time, dia_fin:date, horario_fin:time) -> HttpResponse:
        if not horarios_exactos(horario_inicio, horario_fin):
            return HttpResponse("error: los horarios de comienzo y fin de un turno deben ser horas exactas", status=400)
        if not horarios_dentro_de_rango(dia_inicio, horario_inicio, horario_fin):
            return HttpResponse("error: los horarios superan el limite de la jornada laboral", status=400)
        if not dia_valido(dia_inicio):
            return HttpResponse("error: no se puede sacar un turno para una fecha que ya paso.", status=400)
        if not dia_hora_coherentes(dia_inicio, horario_inicio, dia_fin, horario_fin):
            return HttpResponse("error: un turno no puede terminar antes de que empiece", status=400)
        return HttpResponse("Dias horarios correctos", status=200)        