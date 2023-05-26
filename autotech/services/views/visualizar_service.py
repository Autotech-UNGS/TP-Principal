from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from administracion.models import  Service
from administracion.serializers import ServiceSerializer


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