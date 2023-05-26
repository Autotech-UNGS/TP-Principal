import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.models import Turno_taller
from administracion.serializers import TurnoTallerSerializer
import datetime


class EstadoTurnosViewSet(ViewSet):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_EN_PROCESO = 'en_proceso'
    ESTADO_TERMINADO = 'terminado'
    ESTADO_CANCELADO = 'cancelado'
    ESTADO_RECHAZADO = 'rechazado'
    ESTADO_AUSENTE = 'ausente'

    @action(detail=False, methods=['get'])
    def turnos_pendientes(self, request):
        papeles_en_regla = request.GET.get('papeles_en_regla')
        taller_sup = request.GET.get('branch')
        
        if not ValidadorTaller.es_valido(taller_sup):
            return HttpResponse('error: numero de taller no valido', status=400)  
        if papeles_en_regla is None or (papeles_en_regla.lower() != 'true' and papeles_en_regla.lower() != 'false'):
            return HttpResponse('error: se requiere información sobre si los papeles están en regla o no', status=400)       
       
        id_sucursal = self.obtener_id_taller(taller_sup)
        pendientes = []
        
        if papeles_en_regla.lower() == 'true':
            pendientes += self.obtener_turnos_por_estado(self.ESTADO_PENDIENTE, id_sucursal, tipo='service')
            pendientes += self.obtener_turnos_por_estado(self.ESTADO_PENDIENTE, id_sucursal, tipo='extraordinario')
            pendientes += self.obtener_turnos_por_estado(self.ESTADO_PENDIENTE, id_sucursal, tipo='reparacion')
            pendientes += self.obtener_turnos_por_estado(self.ESTADO_PENDIENTE, id_sucursal, papeles_en_regla=True, tipo='evaluacion') 
        elif papeles_en_regla.lower() == 'false':
            pendientes = self.obtener_turnos_por_estado(self.ESTADO_PENDIENTE, id_sucursal, papeles_en_regla=False, tipo='evaluacion')
       
        serializer = TurnoTallerSerializer(pendientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def turnos_en_proceso(self, request):
        taller_sup = request.GET.get('branch')
        
        if not ValidadorTaller.es_valido(taller_sup):
            return HttpResponse('error: numero de taller no valido', status=400)     
        
        id_sucursal = self.obtener_id_taller(taller_sup)
        en_procesos = self.obtener_turnos_por_estado(self.ESTADO_EN_PROCESO, id_sucursal)
        serializer = TurnoTallerSerializer( en_procesos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)   

    @action(detail=False, methods=['get'])
    def turnos_terminados(self, request):
        taller_sup = request.GET.get('branch')
        
        if not ValidadorTaller.es_valido(taller_sup):
            return HttpResponse('error: numero de taller no valido', status=400)     
        
        id_sucursal = self.obtener_id_taller(taller_sup)
        terminados = self.obtener_turnos_por_estado(self.ESTADO_TERMINADO, id_sucursal)
        serializer = TurnoTallerSerializer(terminados, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)     


    @action(detail=False, methods=['get'])
    def turnos_cancelados(self, request):
        taller_sup = request.GET.get('branch')
        
        if not ValidadorTaller.es_valido(taller_sup):
            return HttpResponse('error: numero de taller no valido', status=400)    
        
        id_sucursal = self.obtener_id_taller(taller_sup)
        cancelados = self.obtener_turnos_por_estado(self.ESTADO_CANCELADO, id_sucursal)     
        serializer = TurnoTallerSerializer(cancelados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def turnos_no_validos(self, request):
        taller_sup = request.GET.get('branch')
        
        if not ValidadorTaller.es_valido(taller_sup):
            return HttpResponse('error: numero de taller no valido', status=400)     
        
        id_sucursal = self.obtener_id_taller(taller_sup)
        rechazados = self.obtener_turnos_por_estado(self.ESTADO_RECHAZADO, id_sucursal)
        ausentes = self.obtener_turnos_por_estado(self.ESTADO_AUSENTE, id_sucursal)
        no_validos = rechazados.union(ausentes)
        serializer = TurnoTallerSerializer(no_validos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)     
   
    @action(detail=True, methods=['patch'])
    def actualizar_estado_turno_en_proceso(self, request, id_turno):  
        try:
            turno = Turno_taller.objects.get(id_turno=id_turno, estado=self.ESTADO_EN_PROCESO)
        except Turno_taller.DoesNotExist:
            return HttpResponse('error: el turno no existe o no esta en proceso', status=400)
        hoy = datetime.date.today()
        ahora = datetime.datetime.now().time()
        
        if hoy < turno.fecha_inicio:
            return HttpResponse('error: el turno no puede ser finalizado antes del día de inicio del mismo', status=400)
        elif hoy == turno.fecha_inicio and ahora < turno.hora_inicio:
            return HttpResponse('error: el turno no puede ser finalizado antes del horario de inicio del mismo', status=400)
        
        turno.estado = self.ESTADO_TERMINADO
        
        turno.save()
        
        return HttpResponse('El turno ha cambiado de estado a terminado exitosamente.')
    
    @action(detail=True, methods=['patch'])
    def cancelar_turno_pendiente(self, request, id_turno):
        try:
            turno = Turno_taller.objects.get(id_turno=id_turno, estado=self.ESTADO_PENDIENTE)
        except Turno_taller.DoesNotExist:
            return HttpResponse('error: el turno no existe o no esta en estado pendiente', status=400) 
        
        turno.estado = self.ESTADO_CANCELADO
        turno.save()   
        return HttpResponse('El turno ha sido cancelado correctamente.')
        
    def obtener_id_taller(self, taller_sup):
        return int(taller_sup[-3:])

    def obtener_turnos_por_estado(self, estado, id_taller, papeles_en_regla=None, tipo=None):
        query = Turno_taller.objects.filter(estado=estado, taller_id=id_taller)
       
        if papeles_en_regla is not None:
            query = query.filter(papeles_en_regla=papeles_en_regla)    
        if tipo is not None:
                query = query.filter(tipo=tipo)
        
        return query

class ValidadorTaller():
       @classmethod
       def es_valido(cls, taller_empleado):
        if taller_empleado is None:
            return False
        if len(taller_empleado) != 4:
            return False
        if taller_empleado[0] != 'T':
            return False
        if not taller_empleado[1:].isdigit():
            return False   
        return True