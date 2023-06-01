from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from administracion.models import Taller, Turno_taller
from administracion.serializers import TallerSerializer, TurnoTallerSerializer

from talleres.validadores import ValidadorTaller

from talleres.api_client.cliente_sucursales import ClientSucursales

import warnings


class ModificarTaller(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, id_taller):
        validador = ValidadorTaller()

        response_data = {
                    "resultado": [],
                    "warnings": []
        }

        # ------------------------------------------------------------------------------------------------------ #
        try:
            taller = Taller.objects.get(id_taller=id_taller)
        except Taller.DoesNotExist:
            return Response({'error': f'El taller {id_taller} no existe'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            validador.validar_datos(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # ------------------------------------------------------------------------------------------------------ #
        print(taller.estado)
        turnos_pendientes = Turno_taller.objects.filter(taller_id=id_taller, estado__in=["en_proceso","pendiente"]).exists()

        if turnos_pendientes and taller.estado:
            warning_message = f'Tener en cuenta que está haciendo INACTIVO un taller con turnos pendientes y/o en procreso (taller = {id_taller}). No se podrá sacar turnos en el taller hasta que esté ACTIVO nuevamente'
            # warnings.warn(warning_message, UserWarning)
            response_data["warnings"].append(warning_message)
        
        if turnos_pendientes and not taller.estado:
            taller.estado = True
        elif taller.estado:
            taller.estado = False
        else:
            taller.estado = True


        # ------------------------------------------------------------------------------------------------------ #
        id_sucursal_nueva = request.data.get("id_sucursal")
        id_sucursal_taller = taller.id_sucursal

        try:
            taller = Taller.objects.get(id_sucursal=id_sucursal_taller)
        except Taller.DoesNotExist:
            return Response({'error': f'No existe un taller para la sucursal {id_sucursal_taller}'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            validador.validar_datos_reasignacion(request, id_taller)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validador.validar_taller(id_sucursal_nueva, id_taller)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)

        taller.id_sucursal = id_sucursal_nueva
        # ------------------------------------------------------------------------------------------------------ #

        serializer = TallerSerializer(taller, data=request.data, partial=True)
        if serializer.is_valid():
            # Excluir los campos de localidad, provincia , código postal, y el id del taller
            excluded_fields = ['id_taller', 'localidad', 'provincia','cod_postal']
            for field in excluded_fields:
                serializer.validated_data.pop(field, None)

            # Guardar los cambios en el taller
            serializer.save()
            response_data["resultado"].append(serializer.data)
   
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data["resultado"].append(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        










class ActualizarTallerAdmin(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, id_sucursal):
        validador = ValidadorTaller()

        try:
            taller = Taller.objects.get(id_sucursal=id_sucursal)
        except Taller.DoesNotExist:
            return Response({'error': f'No existe un taller creado para la sucursal {id_sucursal}'}, status=status.HTTP_404_NOT_FOUND)
        
        # Obetengo los datos actualizados de la sucursal pasada
        localidad_nueva = ClientSucursales.obtener_valor_clave(id_sucursal,"localidad")
        print(localidad_nueva)

        provincia_nueva = ClientSucursales.obtener_valor_clave(id_sucursal,"provincia")
        print(provincia_nueva)

        codigo_postal_nuevo = ClientSucursales.obtener_valor_clave(id_sucursal,"codigo_postal")
        print(codigo_postal_nuevo)


        taller.localidad = localidad_nueva
        taller.provincia = provincia_nueva
        taller.cod_postal = codigo_postal_nuevo

        taller_actualizado = taller

        serializer = TallerSerializer(taller_actualizado)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ActualizarEstado(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, id_taller, format=None):
         
        try:
            taller = Taller.objects.get(id_taller=id_taller)
        except Taller.DoesNotExist:
            return Response({'error': f'No existe un taller para el ID = {id_taller} proporcionado'}, status=status.HTTP_404_NOT_FOUND)
        
        print(taller.estado)
        turnos_pendientes = Turno_taller.objects.filter(taller_id=id_taller, estado__in=["en_proceso","pendiente"]).exists()

        if turnos_pendientes and taller.estado:
            return Response({'error': 'No se puede cambiar el estado. Aún hay turnos asociados a este taller.'}, status=status.HTTP_400_BAD_REQUEST)
        elif turnos_pendientes and not taller.estado:
            taller.estado = True
        elif taller.estado:
            taller.estado = False
        else:
            taller.estado = True
 
        taller.save()

        serializer = TallerSerializer(taller)

        response_data = {
            "taller":serializer.data,
        }
        return Response(serializer.data, status=status.HTTP_200_OK)