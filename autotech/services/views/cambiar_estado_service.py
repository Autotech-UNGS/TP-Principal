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


class ActualizarEstado(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, id_service, format=None):
         
        try:
            service = Service.objects.get(id_service=id_service)
        except Service.DoesNotExist:

            return Response({'error': 'No existe un service para el ID proporcionado'}, status=status.HTTP_404_NOT_FOUND)

        # Realiza las validaciones necesarias para los datos enviados en la solicitud
        # Actualiza el campo deseado
        print(service.activo)
        if service.activo:
            service.activo = False
        else:
            service.activo = True
        service.save()

        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)