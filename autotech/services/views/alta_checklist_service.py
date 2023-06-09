import json

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from administracion.models import Checklist_evaluacion, Checklist_service
from administracion.serializers import ChecklistServiceSerializer

from services.validadores import *



class CopiarChecklistEvaluacion(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        checklist_evaluacion = Checklist_evaluacion.objects.all()

        for item in checklist_evaluacion:
            elemento = item.elemento
            tarea = item.tarea
            costo_reemplazo = item.costo_reemplazo
            duracion_reemplazo = item.duracion_reemplazo

            checklist_service = Checklist_service.objects.create(elemento = elemento, tarea = tarea, costo_reemplazo = costo_reemplazo
                                                                 , duracion_reemplazo = duracion_reemplazo)
            serializer = ChecklistServiceSerializer(checklist_service)

        checklist_evaluacion = Checklist_evaluacion.objects.all()
        serializer = ChecklistServiceSerializer(checklist_evaluacion, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ChecklistEvaluacionListar(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if not Checklist_evaluacion.objects.exists():
            return Response({'error': 'La checklist está vacía'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            checklist = Checklist_evaluacion.objects.all()
            serializer = ChecklistServiceSerializer(checklist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)