import json

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from talleres.validadores import *
from talleres.api_client.cliente_sucursales import ClientSucursales

class VisualizarSucursalesConTallerValidas(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):

        try:
            cliente = ClientSucursales.obtener_sucursales()
        except Exception as e:
            error_messages = str(e)
            return Response({'error': error_messages}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(cliente, status=status.HTTP_200_OK)
    
class VisualizarUnaSucursalConTallerValida(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request,id_sucursal, format=None):

        try:
            cliente = ClientSucursales.obtener_sucursal(id_sucursal)
        except Exception as e:
            error_messages = str(e)
            return Response({'error': error_messages}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(cliente, status=status.HTTP_200_OK)

    
class VisualizarSucursalesSinTaller(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):

        try:
            cliente = ClientSucursales.obtener_sucursales_sin_talller()
        except Exception as e:
            error_messages = str(e)
            return Response({'error': error_messages}, status=status.HTTP_204_NO_CONTENT)
        
        return Response(cliente, status=status.HTTP_200_OK)