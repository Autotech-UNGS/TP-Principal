import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from administracion.models import  Service, Service_tasks, Checklist_service
from administracion.serializers import ServiceSerializer, ServiceTasksSerializer

from services.validadores import *



class ServiceCreate(APIView):
    permission_classes = [permissions.AllowAny]

    # { "marca": "Renault", "modelo": "206", "frecuencia_km":"15000", "costo_base":"10000.0","id_supervisor":"1","id_tasks":"[1,2,3,4,5]"}
    def post(self, request, *args, **kwargs):
        validador = ValidadorService()

        try:
            validador.validar_service(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        marca = (request.data.get('marca')).lower()
        modelo = (request.data.get('modelo')).lower()
        frecuencia_km = request.data.get('frecuencia_km')
        costo_base = request.data.get('costo_base')
        id_supervisor = request.data.get('id_supervisor')
        id_tasks = request.data.get('id_tasks')
        id_task_lista = json.loads(id_tasks)

        try:
            validador.validar_tareas(id_task_lista)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        #print(id_task_lista)

        costo_total, duracion_total = calcular_costo_y_duracion_total(id_task_lista)
        # print(costo_total, duracion_total)
        costo_total += costo_base

        service = Service.objects.create(marca=marca, modelo=modelo, frecuencia_km = frecuencia_km, costo_base = costo_base
                                         , costo_total = costo_total, duracion_total = duracion_total
                                         , id_supervisor = id_supervisor)
        
        service_tasks = Service_tasks.objects.create(id_service = service, id_tasks = id_tasks)

        serializer_tasks = ServiceTasksSerializer(service_tasks)
        serializer_service = ServiceSerializer(service)

        response_data = {
            "service":serializer_service.data,
            "service_tasks":serializer_tasks.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    

def calcular_costo_y_duracion_total(lista):
    costo_total = 0.0
    duracion_total = 0

    for id in lista:
        item = Checklist_service.objects.get(id_task = id)
        costo_total += item.costo_reemplazo
        duracion_total += item.duracion_reemplazo

    return costo_total, duracion_total