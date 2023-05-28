from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from administracion.models import Taller
from administracion.serializers import TallerSerializer

from talleres.validadores import ValidadorTaller


class ModificarTaller(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, id_taller):
        validador = ValidadorTaller()

        try:
            taller = Taller.objects.get(id_taller=id_taller)
        except Taller.DoesNotExist:
            return Response({'error': f'El taller {id_taller} no existe'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            validador.validar_datos(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TallerSerializer(taller, data=request.data, partial=True)
        if serializer.is_valid():
            # Excluir los campos de localidad, provincia y código postal
            serializer.validated_data.pop('localidad', None)
            serializer.validated_data.pop('provincia', None)
            serializer.validated_data.pop('codigo_postal', None)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
