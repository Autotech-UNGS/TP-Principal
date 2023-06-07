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
            return HttpResponse(f"error: el id ingresado no pertenece a ningún turno en el sistema: {id_turno}", status=400)
        if not existe_taller(taller_id):
            return HttpResponse(f"error: el id ingresado no pertenece a ningún taller en el sistema: {taller_id}", status=400)
        if not taller_es_valido(taller_id):
            return HttpResponse(f"error: el id ingresado pertenece a un taller inactivo: {taller_id}", status=400)

        duracion = obtener_duracion(turno.fecha_inicio, turno.hora_inicio, turno.fecha_fin, turno.hora_fin)
        dias_horarios_data = dias_disponibles_desde_hoy_a_cuarentaycinco_dias(taller_id, duracion)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles(self, request, taller_id: int):
        if not existe_taller(taller_id):
            return HttpResponse(f"error: el id ingresado no pertenece a ningún taller en el sistema: {taller_id}", status=400)
        if not taller_es_valido(taller_id):
            return HttpResponse(f"error: el id ingresado pertenece a un taller inactivo: {taller_id}", status=400)

        dias_horarios_data = dias_disponibles_desde_hoy_a_treinta_dias(taller_id, 1)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    
    
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles_service(self, request, taller_id: int, patente:str, km_actual:int):
        patente = patente.upper()
        if not existe_taller(taller_id):
            return HttpResponse(f"error: el id ingresado no pertenece a ningún taller en el sistema: {taller_id}", status=400)
        if not taller_es_valido(taller_id):
            return HttpResponse(f"error: el id ingresado pertenece a un taller inactivo: {taller_id}", status=400)
        if not patente_registrada(patente):
            return HttpResponse(f"error: la patente no está registrada como perteneciente a un cliente: {patente}", status=400)
        km_actual = redondear_a_multiplo_de_cincomil(km_actual)
        km_solicitado = obtener_frecuencia_service_solicitado(patente=patente, kilometraje_actual=km_actual)
        duracion = obtener_duracion_service_vehiculo(patente, km_solicitado)
        if duracion == 0:
            return HttpResponse("error: no existe un service con los datos especificados", status=400)
        dias_horarios_data = dias_disponibles_desde_hoy_a_treinta_dias(taller_id, duracion)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})
    
    
    @action(detail=True, methods=['get'])
    def dias_horarios_disponibles_reparaciones(self, request, taller_id: int, patente:str, origen:str):
        patente = patente.upper()
        if not existe_taller(taller_id):
            return HttpResponse(f"error: el id ingresado no pertenece a ningún taller en el sistema: {taller_id}", status=400)
        if not taller_es_valido(taller_id):
            return HttpResponse(f"error: el id ingresado pertenece a un taller inactivo: {taller_id}", status=400)

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
    
def taller_es_valido(taller_id:int):
    taller = Taller.objects.get(id_taller= taller_id)
    return taller.estado == True

def patente_registrada(patente:str):
    existe_patente = ClientVehiculos.patente_registrada_vendido(patente=patente)
    return existe_patente
       