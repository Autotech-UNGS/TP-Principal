from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from administracion.models import  Service, Checklist_service, Service_tasks, Registro_service, Turno_taller
from administracion.serializers import ServiceSerializer, ChecklistServiceSerializer, TurnoTallerSerializer

from services.views import registro_info_service
from vehiculos.api_client.vehiculos import ClientVehiculos


import json


# -----------------------------------------------------------------------------------------------------
#------------------------------------SERVICES LEER TODOS-----------------------------------------------
# -----------------------------------------------------------------------------------------------------
class VisualizarServiceList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if not Service.objects.exists():
            return Response({'error': 'No hay services cargados actualmente'}, status=status.HTTP_204_NO_CONTENT)
        else:
            service = Service.objects.all()
            serializer = ServiceSerializer(service, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)


# -----------------------------------------------------------------------------------------------------
#------------------------------------SERVICES LEER UNO-------------------------------------------------
# -----------------------------------------------------------------------------------------------------
class VisualizarServiceUno(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_service, format=None):
        if not Service.objects.filter(id_service=id_service).exists():
             return Response({'error': 'No existen service para el id proporcionado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            service = Service.objects.filter(id_service=id_service)
            serializer = ServiceSerializer(service, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
# -----------------------------------------------------------------------------------------------------
#------------------------------------SERVICES LEER TAREAS----------------------------------------------
# -----------------------------------------------------------------------------------------------------
class VisualizarTareasService(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_service, format=None):
        if not Service.objects.filter(id_service=id_service).exists():
             return Response({'error': 'No existen service para el id proporcionado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            id_tasks = Service_tasks.objects.get(id_service = id_service).id_tasks
            id_tasks_lista = json.loads(id_tasks)
            tasks = Checklist_service.objects.filter(id_task__in=id_tasks_lista)

            serializer = ChecklistServiceSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------------------------------
#------------------------------------VISUALIZAR TAREAS DE TURNO DE SERVICE-----------------------------
# -----------------------------------------------------------------------------------------------------
class VisualizarTareasServicePorTurno(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_turno, format=None):

        if not Turno_taller.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        turno = Turno_taller.objects.get(id_turno=id_turno)

        if not turno.tipo == "service":
            return Response({'error': 'El turno pasado no es un turno para Service'}, status=status.HTTP_400_BAD_REQUEST)
    
        if not turno.estado == "en_proceso":
            return Response({'error': 'El turno pasado no está en estado en proceso'}, status=status.HTTP_400_BAD_REQUEST)
        
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

        
        patente_del_turno = turno.patente
        modelo = ClientVehiculos.obtener_modelo(patente_del_turno)
        marca = ClientVehiculos.obtener_marca(patente_del_turno)
        km_del_turno = turno.frecuencia_km

        print(f'patene: {patente_del_turno}, marca: {marca}, modelo: {modelo}, km: {km_del_turno}')

        id_service = registro_info_service.obtener_service(modelo,marca,km_del_turno)
        
        print(f'id service: {id_service}')


        id_tasks = Service_tasks.objects.get(id_service = id_service).id_tasks
        id_tasks_lista = json.loads(id_tasks)
        tasks = Checklist_service.objects.filter(id_task__in=id_tasks_lista)

        serializer = ChecklistServiceSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# -----------------------------------------------------------------------------------------------------
#------------------------------------VISUALIZAR PRECIO DE SERVICE-------------------------------------
# -----------------------------------------------------------------------------------------------------
class VisualizarPrecioService(APIView):
    permission_classes = [permissions.AllowAny]
    # id_turno = 252
    def get(self, request, id_turno, format=None):
        # id_turno = request.data.get('id_turno')
        id_tasks_reemplazadas = request.data.get('id_tasks_remplazadas')

        if not Turno_taller.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        turno = Turno_taller.objects.get(id_turno=id_turno)

        if not turno.tipo == "service":
            return Response({'error': 'El turno pasado no es un turno para Service'}, status=status.HTTP_400_BAD_REQUEST)
    
        if not turno.estado == "en_proceso":
            return Response({'error': 'El turno pasado no está en estado en proceso'}, status=status.HTTP_400_BAD_REQUEST)
        
# -----------------------------------------------------------------------------------------------------
        tiene_garantia = False #verificar_garantia() metodo luci aun no hecho 

# -----------------------------------------------------------------------------------------------------

        patente_del_turno = turno.patente
        modelo = ClientVehiculos.obtener_modelo(patente_del_turno)
        marca = ClientVehiculos.obtener_marca(patente_del_turno)
        km_del_turno = turno.frecuencia_km
        print(f'patente: {patente_del_turno}, marca: {marca}, modelo: {modelo}, km: {km_del_turno}')

        id_service = registro_info_service.obtener_service(modelo,marca,km_del_turno)
        print(f'id service: {id_service}')

        id_tasks_lista = json.loads(id_tasks_reemplazadas)
        print(f'partes a reemplazar {id_tasks_lista}')
        costo_final_service = registro_info_service.obtener_costo_final_service(tiene_garantia, id_service, id_tasks_lista)

        response_data = {
            "precio": costo_final_service
        }

        return Response(response_data, status=status.HTTP_200_OK)