import json

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
    
    # marca, modelo, frecuencia_km, costo_base, id_supervisor, id_tasks
    # { "marca": "Renault", "modelo": "206", "frecuencia_km":"15000", "costo_base":"10000.0","id_supervisor":"1","id_tasks":"[1,2,3,4,5]"}
    def post(self, request, *args, **kwargs):
        validador = ValidadorService()
        try:
            validador.validar_service(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        
        marca = request.data.get('marca')
        modelo = request.data.get('modelo')
        frecuencia_km = request.data.get('frecuencia_km')
        costo_base = request.data.get('costo_base')
        id_supervisor = request.data.get('id_supervisor')

        # capturo las id_tasks que son del service creado y calculo su duracion y costo total
        id_tasks = request.data.get('id_tasks')
        id_task_lista = json.loads(id_tasks)
        #print(id_task_lista)

        costo_total, duracion_total = calcular_costo_y_duracion_total(id_task_lista)
        # print(costo_total, duracion_total)
        costo_total += costo_base

        marca = marca.lower()
        modelo = modelo.lower()


        service = Service.objects.create(marca=marca, modelo=modelo, frecuencia_km = frecuencia_km, costo_base = costo_base
                                         , costo_total = costo_total, duracion_total = duracion_total
                                         , id_supervisor = id_supervisor)
        serializer = ServiceSerializer(service)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


    """ if not Turno_taller.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        turno = Turno_taller.objects.get(id_turno = id_turno)
        if not turno.tipo == "evaluacion":
            return Response({'error': 'El turno pasado no es un turno para Evaluación'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Registro_evaluacion.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado ya existe en los registros'}, status=status.HTTP_400_BAD_REQUEST)
        # Tomo el turno que corresponde a ese id
        turno_taller = Turno_taller.objects.get(pk=id_turno) """
    

def calcular_costo_y_duracion_total(lista):
    costo_total = 0.0
    duracion_total = 0

    for id in lista:
        item = Checklist_service.objects.get(id_task = id)
        costo_total += item.costo_reemplazo
        duracion_total += item.duracion_reemplazo

    return costo_total, duracion_total