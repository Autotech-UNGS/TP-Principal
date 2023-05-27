from django.http import JsonResponse, HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from ..obtener_datos import *
from ..validaciones_views import * 
from datetime import *
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

class AsignarTecnicoViewSet(ViewSet):        
        
    @action(detail=True, methods=['get'])
    def tecnicos_disponibles(self, request, id_turno: int):
        try:
            turno=Turno_taller.objects.get(id_turno=id_turno)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        else:
            tecnicos_disponibles = obtener_tecnicos_disponibles(turno.id_turno, turno.taller_id.id_taller)
            resultado = [{'id_tecnico': tecnico} for tecnico in tecnicos_disponibles]
            return JsonResponse({'tecnicos_disponibles':resultado})
        

    @action(detail=True, methods=['post'])
    def asignar_tecnico(self, request, id_tecnico:int, id_turno: int):
        try:
            turno=Turno_taller.objects.get(id_turno=id_turno)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        else:
            tipo_turno = turno.tipo
            papeles_en_regla_turno = turno.papeles_en_regla
            dia_inicio_turno = turno.fecha_inicio
            hora_inicio_turno = turno.hora_inicio
            dia_fin_turno = turno.fecha_fin
            hora_fin_turno = turno.hora_fin
            tecnico_asignado = turno.tecnico_id
            
            if tecnico_asignado != None:
                return HttpResponse("error: el turno ya fue asignado.", status=400)
            if not coinciden_los_talleres(id_tecnico, turno.taller_id.id_taller):
                return HttpResponse("error: el turno no esta asignado al taller donde el tecnico trabaja.", status=400)
            if not se_puede_asignar_tecnico(tipo_turno, papeles_en_regla_turno):
                return HttpResponse("error: administracion no ha aprobado la documentacion.", status=400)
            if not tecnico_esta_disponible(id_tecnico,dia_inicio_turno, hora_inicio_turno, dia_fin_turno, hora_fin_turno):
                return HttpResponse("error: el tecnico no tiene disponible ese horario", status=400)
            
            turno.tecnico_id = id_tecnico  # agregamos el id del tecnico al turno
            turno.save()
            turno.estado = "en_proceso" # cambiamos el estado del turno
            turno.save()
            
            serializer= TurnoTallerSerializer(turno,many=False) # retornamos el turno, donde debería verse el tecnico recien asignado
            return Response(serializer.data)