from django.db.models import Max, F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.models import Registro_service
from administracion.serializers import  RegistroServiceSerializer


class RegistroServiceAdminViewSet(ViewSet):  
    @action(detail=False, methods=['get'])
    def list(self, request):
        registros= Registro_service.objects.all()
        serializer= RegistroServiceSerializer(registros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def obtener_ultimo_registro_patente(self, request, patente):
        registros = Registro_service.objects.filter(id_turno__patente=patente, id_turno__estado='terminado').annotate(
            max_fecha_registro=Max('fecha_registro')
        ).filter(fecha_registro=F('max_fecha_registro'))

        serializer = RegistroServiceSerializer(registros, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)