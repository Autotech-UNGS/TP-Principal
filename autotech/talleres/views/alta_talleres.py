import json

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from administracion.models import Taller
from administracion.serializers import TallerSerializer
from talleres.validadores import *
from talleres.api_client.cliente_sucursales import ClientSucursales

# id (sucursal),nombre, direccion, mail, telefono, capacidad, cant_tecnicos
# localidad, provincia, codigo_postal = sucursal
class TalleresCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        validador = ValidadorTaller()

        try:
            validador.validar_datos(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        id_sucursal = request.data.get("id_sucursal")
        nombre = request.data.get("nombre")
        direccion =  request.data.get("direccion")
        mail =  request.data.get("mail")
        telefono =  request.data.get("telefono")
        capacidad =  request.data.get("capacidad")
        cant_tecnicos = request.data.get("cant_tecnicos")

        try:
            validador.validar_taller(id_sucursal)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        # localidad, provincia, codigo_postal = sucursal
        localidad = ClientSucursales.obtener_valor_clave(id_sucursal,"localidad")
        provincia = ClientSucursales.obtener_valor_clave(id_sucursal,"provincia")
        codigo_postal = ClientSucursales.obtener_valor_clave(id_sucursal,"codigo_postal")

        taller = Taller.objects.create(nombre=nombre
                                       , direccion=direccion
                                       , mail=mail
                                       , telefono=telefono
                                       , capacidad=capacidad
                                       , cant_tecnicos=cant_tecnicos
                                       , localidad=localidad
                                       , provincia=provincia
                                       , cod_postal=codigo_postal
                                       , id_sucursal = id_sucursal)

        serializer = TallerSerializer(taller)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    