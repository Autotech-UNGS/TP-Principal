import json
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction

from administracion.models import Registro_evaluacion_admin, Id_task_puntaje, Registro_evaluacion
from administracion.serializers import  RegistroEvaluacionAdminSerializer, IdTaskPuntajeSerializer, RegistroEvaluacionSerializer


# -----------------------------------------------------------------------------------------------------

class RegistroEvaluacionAdminReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Registro_evaluacion_admin.objects.all()
    serializer_class = RegistroEvaluacionAdminSerializer
    permission_classes = [permissions.AllowAny]

class RegistroEvaluacionAdminCreateViewSet(viewsets.ModelViewSet):
    queryset = Registro_evaluacion_admin.objects.all()
    serializer_class = RegistroEvaluacionAdminSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# -----------------------------------------------------------------------------------------------------
class 
    
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionReadOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = Registro_evaluacion.objects.all()
    serializer_class = RegistroEvaluacionSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        # Obtén los registros del modelo Registro_evaluacion
        registros = self.queryset

        # Recorre la otra tabla y realiza alguna acción adicional
        otra_tabla = Id_task_puntaje.objects.all()
        primer_fila = Id_task_puntaje.objects.first() 
        
        if primer_fila is not None: # Obtener la primera fila de la tabla
            id_turno = primer_fila.id_turno  # Obtener el valor de la columna 'id_turno'
            datos_diccionario = {}
            for fila in otra_tabla:
                # Hacer algo con los datos de la fila de otra tabla
                checklist_evaluacion_id = fila.id_task.id_task
                puntaje_seleccionado = fila.puntaje_seleccionado
                datos_diccionario[str(checklist_evaluacion_id)] = puntaje_seleccionado

            registro_nuevo = Registro_evaluacion()
            registro_nuevo.id_turno = id_turno
            registro_nuevo.id_task_puntaje = datos_diccionario
            registro_nuevo.save()
        if Id_task_puntaje.objects.exists():
            Id_task_puntaje.objects.all().delete()
        # Llama al método 'list' de la clase padre para obtener la respuesta
        response = super().list(request, *args, **kwargs)

        # Devuelve la respuesta actualizada
        return response
