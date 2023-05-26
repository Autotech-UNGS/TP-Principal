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
            registros = Service.objects.all()
            serializer = ServiceSerializer(registros, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)