import requests
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.serializers import TurnoTallerSerializer
from administracion.models import Turno_taller
from .validadores_views import ValidadorDatosTecnico, ValidadorDatosSupervisor
from .consumidor_api_externa import ConsumidorApiTecnicos


class TecnicoViewSet(ViewSet):
    validador_tec = ValidadorDatosTecnico()
    validador_sup = ValidadorDatosSupervisor()

    @action(detail=False, methods=['get'])
    def lista_tecnicos(self, request):
        sucursal_supervisor = request.GET.get('branch')     
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse('error: numero de sucursal no valido', status=400)
        tecnicos =ConsumidorApiTecnicos.consumir_tecnicos(sucursal_supervisor)
        return JsonResponse({'tecnicos': tecnicos})

    @action(detail=True, methods=['get'])
    def detalle_trabajos_tecnico(self, request, id_tecnico):
        sucursal_supervisor = request.GET.get('branch')       
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse('error: numero de sucursal no valido', status=400)      
        id_sucursal = int(sucursal_supervisor[-3:])
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, taller_id=id_sucursal).order_by('estado')
        data = []
        for turno in turnos:
            data.append({
                "id_turno": turno.id_turno,
                "patente": turno.patente,
                "fecha_inicio": turno.fecha_inicio,
                "hora_inicio": turno.hora_inicio,
                "fecha_fin": turno.fecha_fin,
                "hora_fin": turno.hora_fin,
                "tipo": turno.tipo,
                "estado": turno.estado
            })
        return Response(data)

    @action(detail=True, methods=['get'])
    def trabajos_en_proceso_tecnico(self, request, id_tecnico):
        sucursal_supervisor = request.GET.get('branch')       
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse('error: numero de sucursal no valido', status=400)
        id_sucursal = int(sucursal_supervisor[-3:])
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, taller_id=id_sucursal, estado='en_proceso')
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])   
    def trabajos_terminados_tecnico(self, request, id_tecnico):
        sucursal_supervisor = request.GET.get('branch')       
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse('error: numero de sucursal no valido', status=400) 
        id_sucursal = int(sucursal_supervisor[-3:]) 
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, taller_id=id_sucursal, estado='terminado')
        serializer= TurnoTallerSerializer(turnos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categorias(self, request):
        """Devuelve una lista de todas las categorías de técnico disponibles.
        """
        tipos_categorias = ["A", "B", "C", "D"]
        return JsonResponse(tipos_categorias, safe=False)

    @action(detail=False, methods=['get'])
    def filtrar_tecnicos(self, request):
        sucursal_supervisor = request.GET.get('branch')
        categoria = request.GET.get('categoria')
        dni = request.GET.get('dni')
        nombre = request.GET.get('nombre_completo')
        if not self.validador_sup.sucursal(sucursal_supervisor):
            return HttpResponse('error: numero de sucursal no valido', status=400)
        if not self.validador_tec.categoria(categoria=categoria):
            return HttpResponse('error: categoría no valida', status=400)
        if not self.validador_tec.dni(dni=dni):
            return HttpResponse('error: DNI no valido', status=400)
        try:
            tecnicos = self.obtener_tecnicos(sucursal_supervisor, categoria, dni, nombre)
            return JsonResponse({'tecnicos': tecnicos})
        except requests.HTTPError as e:
            return HttpResponse(str(e), status=e.response.status_code)
    
    def obtener_tecnicos(self, sucursal_supervisor, categoria=None, dni=None, nombre=None):
        tecnicos = ConsumidorApiTecnicos.consumir_tecnicos(sucursal_supervisor)
        if categoria is not None:
            tecnicos = [tecnico for tecnico in tecnicos if tecnico['categoria'] == categoria]
        if dni is not None:
            tecnicos = [tecnico for tecnico in tecnicos if tecnico['dni'] == dni]  
        if nombre is not None:
            tecnicos = [tecnico for tecnico in tecnicos if nombre.lower() in tecnico['nombre_completo'].lower()]
        if not tecnicos:
            return []
        return tecnicos
    

