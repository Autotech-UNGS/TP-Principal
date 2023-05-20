from django.http import JsonResponse, HttpResponse, HttpRequest
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from .enviar_turno_email import EnvioDeEmail
from django.http import QueryDict
from .obtener_datos_usuario import *
from .validaciones_views import * 
from datetime import *

class CrearActualizarTurnosViewSet(ViewSet):
    @action(detail=True, methods=['get'])
    def diasHorariosDisponibles(self, request, taller_id: int):
        try:
            taller = Taller.objects.get(id_taller= taller_id)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)
        else:
            dias_horarios_data = dias_horarios_disponibles_treinta_dias(taller_id)
            resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
            return JsonResponse({'dias_y_horarios':resultado})
    
    # esta vista es para:
        # para cuando el cliente saca un turno en la página --> saca para service y para evaluación
    @action(detail=False, methods=['post'])
    def crearTurno(self, request):
        dia = request.data.get("fecha_inicio")
        dia_fin = request.data.get("fecha_fin")
        horario_inicio = request.data.get("hora_inicio")
        horario_fin = request.data.get("hora_fin")
        taller_id = request.data.get("taller_id")
        tipo = request.data.get("tipo")
        km = request.data.get("frecuencia_km")

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
        
        serializer=TurnoTallerSerializer(data=request.data)
        if serializer.is_valid():
            if tipo == 'evaluacion':
                 serializer.validated_data['papeles_en_regla'] = False
            serializer.save()
            if tipo == 'evaluacion' or tipo == 'service':   
                #email_usuario = request.META.get('email') # obtenemos 'email' del header. Otra opcion es request.headers.get('NombreEncabezado')
                email_usuario = obtener_email_usuario()
                direccion_taller = obtener_direccion_taller(taller_id)
                EnvioDeEmail.enviar_correo(tipo, email_usuario, dia_inicio_date, horario_inicio_time, direccion_taller)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def turnoUpdate(self, request, id_turno):
        try:
            turno=Turno_taller.objects.get(id_turno=id_turno)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        else:
            serializer=TurnoTallerSerializer(instance=turno,data=request.data)
            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data)