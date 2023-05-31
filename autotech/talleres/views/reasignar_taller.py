from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from administracion.models import Taller
from administracion.serializers import TallerSerializer

from talleres.validadores import ValidadorTaller


class ReasignarTaller(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request):
        validador = ValidadorTaller()

        id_sucursal_vieja = request.data.get("id_sucursal_vieja")
        id_sucursal_nueva = request.data.get("id_sucursal_nueva")

        if id_sucursal_vieja == id_sucursal_nueva:
              return Response({'error': f'Estás reasignando el taller de la sucursal {id_sucursal_vieja} a la misma sucursal {id_sucursal_nueva}'}, status=status.HTTP_404_NOT_FOUND)

        try:
            taller = Taller.objects.get(id_sucursal=id_sucursal_vieja)
        except Taller.DoesNotExist:
            return Response({'error': f'No existe un taller para la sucursal {id_sucursal_vieja}'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            validador.validar_datos_reasignacion(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            validador.validar_taller(id_sucursal_nueva)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)

        taller.id_sucursal = id_sucursal_nueva
        taller.save()
        serializer = TallerSerializer(taller)

        return Response(serializer.data, status=status.HTTP_200_OK)
