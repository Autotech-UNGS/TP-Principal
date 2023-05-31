from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.models import *
from ..obtener_datos import *
from ..validaciones_asignar_tecnico import * 
from datetime import *    
from ..obtener_datos import *
from ..gestion_agenda.gestionar_agenda import *
    
class DiasHorariosDisponiblesViewSet(ViewSet):    
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles_turno(self, request, taller_id: int, id_turno:int):
        turno = obtener_turno(id_turno)
        if turno == None:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)

        duracion = obtener_duracion(turno.fecha_inicio, turno.hora_inicio, turno.fecha_fin, turno.hora_fin)
        dias_horarios_data = dias_disponibles_desde_hoy_a_cuarentaycinco_dias(taller_id, duracion)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles(self, request, taller_id: int):
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)

        dias_horarios_data = dias_disponibles_desde_hoy_a_treinta_dias(taller_id, 1)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    
    
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles_service(self, request, taller_id: int, marca:str, modelo:str, km:int):
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)

        duracion = obtener_duracion_service(marca, modelo, km)
        if duracion == 0:
            return HttpResponse("error: no existe un service con los datos especificados", status=400)
        dias_horarios_data = dias_disponibles_desde_hoy_a_treinta_dias(taller_id, duracion)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    
    
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles_reparaciones(self, request, taller_id: int, patente:str, origen:str):
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)

        duracion =  obtener_duracion_extraordinario(patente) if origen == 'extraordinario' else obtener_duracion_reparacion(patente)
        if duracion == 0:
            return HttpResponse("error: la patente no pertenece a la de un auto que ya haya sido evaluado en el taller.", status=400)
        
        dias_horarios_data = dias_disponibles_desde_hoy_a_cuarentaycinco_dias(taller_id, duracion)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    
def existe_taller(taller_id:int):
    try:
        taller = Taller.objects.get(id_taller= taller_id)
    except:
        return False
    else:
        return True
       