from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from administracion.models import  Service, Checklist_service, Service_tasks, Registro_service, Turno_taller
from administracion.serializers import ServiceSerializer, ChecklistServiceSerializer, TurnoTallerSerializer

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
#------------------------------------REGISTROS SERVICE-------------------------------------------------
# -----------------------------------------------------------------------------------------------------
class ListarTurnosRegistroPendienteTecnico(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_tecnico, format=None):
        
        # El técnico pasado no tiene turnos de service en proceso actualmente 
        """  if not Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='evaluacion'):
            return Response({'error': 'El ID del técnico no es válido con un turno de evaluación vigente'}, status=status.HTTP_400_BAD_REQUEST) """
        
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='service')
        id_turnos = list(turnos.values_list('id_turno', flat=True))

        # El técnico no tiene registros de service guardados
        if not Registro_service.objects.filter(id_turno__in = id_turnos):
            serializer = TurnoTallerSerializer(turnos, many=True)
            # Si no tiene turnos registrados de service entonces devuelvo todos los turnos que tenga 
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        registros = Registro_service.objects.filter(id_turno__in = id_turnos) 
        id_turnos_registros = list(registros.values_list('id_turno', flat=True))

        turnos_pendientes_de_registro = Turno_taller.objects.filter(id_turno__in = id_turnos).exclude(id_turno__in = id_turnos_registros)
        serializer = TurnoTallerSerializer(turnos_pendientes_de_registro, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)