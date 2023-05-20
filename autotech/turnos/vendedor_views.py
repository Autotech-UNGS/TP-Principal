from django.http import JsonResponse, HttpResponse, HttpRequest
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from .enviar_turno_email import EnvioDeEmail
from django.http import QueryDict
from .obtener_datos_usuario import *
from .validaciones_views import * 
from datetime import *
    
class CrearTurnoVendedor(ViewSet):
    # los papeles son True por defecto, no hay que modificar el estado de los papeles. El email llega como un dato del json
    @action(detail=False, methods=['post'])
    def crear_turno_vendedor(self, request):
        dia = request.data.get("fecha_inicio")
        dia_fin = request.data.get("fecha_fin")
        horario_inicio = request.data.get("hora_inicio")
        horario_fin = request.data.get("hora_fin")
        taller_id = request.data.get("taller_id")
        tipo = request.data.get("tipo")
        km = request.data.get("frecuencia_km")
        email = request.data.get("email")

        horario_inicio_time = datetime.strptime(horario_inicio, '%H:%M:%S').time()
        horario_fin_time = datetime.strptime(horario_fin, '%H:%M:%S').time()
        dia_inicio_date = datetime.strptime(dia, '%Y-%m-%d').date()
        dia_fin_date = datetime.strptime(dia_fin, '%Y-%m-%d').date()

        if tipo == "service" and km == None:
            return HttpResponse("error: el service debe tener un kilometraje asociado", status=400)
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)
        if not horarios_exactos(horario_inicio_time, horario_fin_time):
            return HttpResponse("error: los horarios de comienzo y fin de un turno deben ser horas exactas", status=400)
        if not horarios_dentro_de_rango(dia_inicio_date, horario_inicio_time, horario_fin_time):
            return HttpResponse("error: los horarios superan el limite de la jornada laboral", status=400)
        if not dia_valido(dia_inicio_date):
            return HttpResponse("error: no se puede sacar un turno para una fecha que ya paso.", status=400)
        if not dia_hora_coherentes(dia_inicio_date, horario_inicio_time, dia_fin_date, horario_fin_time):
            return HttpResponse("error: un turno no puede terminar antes de que empiece", status=400)
        if not taller_esta_disponible(taller_id, dia_inicio_date, horario_inicio_time, dia_fin_date , horario_fin_time):
            return HttpResponse("error: ese dia no esta disponible en ese horario", status=400)
        
        datos = request.data.copy()
        del datos['email']
        serializer = TurnoTallerSerializer(data=datos)
        
        if serializer.is_valid():
            serializer.validated_data['papeles_en_regla'] = True
            if tipo == 'evaluacion' or tipo == 'service':   
                direccion_taller = obtener_direccion_taller(taller_id)
                EnvioDeEmail.enviar_correo(tipo, email, dia_inicio_date, horario_inicio_time, direccion_taller)
        return Response(serializer.data)
    
class ModificarEstadosVendedor(ViewSet):    
    # el estado de los papeles del turno pasa a ser True
    @action(detail=True, methods=['post'])
    def aceptar_papeles(self, request, id_turno):
        try:
            turno = Turno_taller.objects.get(id_turno = id_turno)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        else:
            if turno.tipo != 'evaluacion':
                return HttpResponse("error: el id ingresado no pertenece a un turno de tipo evaluacion, por lo que no tiene estado de papeles", status=400)
            if turno.estado == 'rechazado':
                return HttpResponse("error: el id ingresado pertenece a un turno que ya fue rechazado", status=400)
            elif turno.estado != 'pendiente':
                return HttpResponse(f"error: el id ingresado pertenece a un turno que ya no esta pendiente: {turno.estado}", status=400)
            
            turno.papeles_en_regla = True
            turno.save()
            serializer= TurnoTallerSerializer(turno,many=False) # retornamos el turno, donde debería verse el estado de los papeles True
            return Response(serializer.data)
    
    # el estado del turno pasa a ser rechazado
    @action(detail=True, methods=['post'])
    def rechazar_papeles(self, request, id_turno):
        try:
            turno = Turno_taller.objects.get(id_turno = id_turno)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        else:
            if turno.tipo != 'evaluacion':
                return HttpResponse("error: el id ingresado no pertenece a un turno de tipo evaluacion, por lo que no tiene estado de papeles", status=400)
            if turno.estado != 'pendiente':
                return HttpResponse(f"error: el id ingresado pertenece a un turno que ya no esta pendiente: {turno.estado}", status=400)
            
            turno.papeles_en_regla = False
            turno.save()
            turno.estado = 'rechazado'
            turno.save()
            serializer= TurnoTallerSerializer(turno,many=False) # retornamos el turno, donde debería verse el estado del turno rechazado
            return Response(serializer.data)
    
    