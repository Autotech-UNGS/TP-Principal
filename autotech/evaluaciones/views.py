import json
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



from administracion.models import  Turno_taller, Registro_evaluacion_para_admin, Registro_evaluacion
from administracion.serializers import  RegistroEvaluacionXAdminSerializer, RegistroEvaluacionSerializer


# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionXAdminCreate(viewsets.ModelViewSet):
    queryset = Registro_evaluacion_para_admin.objects.all()
    serializer_class = RegistroEvaluacionXAdminSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RegistroEvaluacionXAdminReadOnly(viewsets.ReadOnlyModelViewSet):
    queryset = Registro_evaluacion_para_admin.objects.all()
    serializer_class = RegistroEvaluacionXAdminSerializer
    permission_classes = [permissions.AllowAny]

    
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionCreate(APIView):
    permission_classes = [permissions.AllowAny]
    
    # id_turno y diccionario ["id_task_puntaje":{"1":20, "2":30}]
    def post(self, request, *args, **kwargs):
        id_turno = request.data.get('id_turno')
        id_task_puntaje = request.data.get('id_task_puntaje')

        # Tomo el turno que corresponde a ese id
        turno_taller = Turno_taller.objects.get(pk=id_turno)
        
        # Realizar validaciones de datos y crear objeto
        registro_evaluacion = Registro_evaluacion.objects.create(id_turno = turno_taller, id_task_puntaje=id_task_puntaje)

        # Serializar objeto y devolver respuesta
        serializer = RegistroEvaluacionSerializer(registro_evaluacion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# -----------------------------------------------------------------------------------------------------
