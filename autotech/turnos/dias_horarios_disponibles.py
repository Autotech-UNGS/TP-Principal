from django.http import JsonResponse, HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from .enviar_turno_email import EnvioDeEmail
from .obtener_datos_usuario import *
from .validaciones_views import * 
from datetime import *    
    
class DiasHorariosDisponiblesViewSet(ViewSet):    
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles_una_hora(self, request, taller_id: int):
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)

        dias_horarios_data = dias_horarios_disponibles_treinta_dias(taller_id, 1)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    
    """
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles_service(self, request, taller_id: int, km:int):
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)

        duracion = ????
        dias_horarios_data = dias_horarios_disponibles_treinta_dias(taller_id, duracion)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    """        