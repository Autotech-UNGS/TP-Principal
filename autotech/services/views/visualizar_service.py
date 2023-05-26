from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from administracion.models import  Service, Checklist_service, Service_tasks
from administracion.serializers import ServiceSerializer, ChecklistServiceSerializer

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
        