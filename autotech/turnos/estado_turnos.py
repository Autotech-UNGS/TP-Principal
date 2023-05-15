import requests
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.models import Turno_taller
from .validaciones_views import ValidadorSupervisor


class EstadoTurnosViewSet(ViewSet):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_EN_PROCESO = 'en_proceso'
    ESTADO_TERMINADO = 'terminado'
    validador_sup = ValidadorSupervisor()

    @action(detail=False, methods=['get'])
    def turnos_pendientes(self, request):
        sucursal_supervisor = request.GET.get('branch')
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse({'error': 'Numero de sucursal no valido'}, status=400)      
        id_sucursal = self.obtener_id_sucursal(sucursal_supervisor)
        pendientes = self.obtener_turnos_por_estado(self.ESTADO_PENDIENTE, id_sucursal)
        turnos_data = self.obtener_turnos_data(pendientes)
        return Response(turnos_data)

    @action(detail=False, methods=['get'])
    def turnos_en_proceso(self, request):
        sucursal_supervisor = request.GET.get('branch')
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse({'error': 'Numero de sucursal no valido'}, status=400)     
        id_sucursal = self.obtener_id_sucursal(sucursal_supervisor)
        en_procesos = self.obtener_turnos_por_estado(self.ESTADO_EN_PROCESO, id_sucursal)
        turnos_data = self.obtener_turnos_data(en_procesos)
        
        return Response(turnos_data)

    @action(detail=False, methods=['get'])
    def turnos_terminados(self, request):
        sucursal_supervisor = request.GET.get('branch')
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse({'error': 'Numero de sucursal no valido'}, status=400)     
        id_sucursal = self.obtener_id_sucursal(sucursal_supervisor)
        terminados = self.obtener_turnos_por_estado(self.ESTADO_TERMINADO, id_sucursal)
        turnos_data = self.obtener_turnos_data(terminados)     
        return Response(turnos_data)
    
    @action(detail=True, methods=['patch'])
    def actualizar_estado_turno_en_proceso(self, request, pk):
        sucursal_supervisor = request.GET.get('branch')
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse({'error': 'Numero de sucursal no valido'}, status=400)      
        id_sucursal = self.obtener_id_sucursal(sucursal_supervisor)     
        try:
            turno = Turno_taller.objects.get(id_turno=pk, estado=self.ESTADO_EN_PROCESO, taller_id=id_sucursal)
        except Turno_taller.DoesNotExist:
            return HttpResponse({'error': 'El turno no existe o no está en proceso'}, status=400)      
        turno.estado = self.ESTADO_TERMINADO
        turno.save()
        turnos_en_proceso = self.obtener_turnos_por_estado(self.ESTADO_EN_PROCESO, id_sucursal)
        turnos_data = self.obtener_turnos_data(turnos_en_proceso)       
        return Response(turnos_data)
    
    def obtener_id_sucursal(self, sucursal_supervisor):
        return int(sucursal_supervisor[-3:])

    def obtener_turnos_por_estado(self, estado, id_sucursal):
        return Turno_taller.objects.filter(estado=estado, taller_id=id_sucursal)

    def obtener_turnos_data(self, turnos):
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
