import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError


from administracion.models import  Turno_taller, Registro_evaluacion_para_admin, Registro_evaluacion, Checklist_evaluacion
from administracion.serializers import  RegistroEvaluacionXAdminSerializerGET, RegistroEvaluacionSerializer, ChecklistEvaluacionSerializer
from .validadores import ValidadorChecklist

# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION CREAR-----------------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionCreate(APIView):
    permission_classes = [permissions.AllowAny]
    
    # id_turno , diccionario ["id_task_puntaje":{"1":20, "2":30}], detalle 
    def post(self, request, *args, **kwargs):
        validador = ValidadorChecklist()
        try:
            validador.validar_diccionario(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        id_turno = request.data.get('id_turno')
        id_task_puntaje = request.data.get('id_task_puntaje')

        detalle = request.data.get('detalle')

        if not Turno_taller.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        turno = Turno_taller.objects.get(id_turno = id_turno)
        if not turno.tipo == "evaluacion":
            return Response({'error': 'El turno pasado no es un turno para Evaluación'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Registro_evaluacion.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado ya existe en los registros'}, status=status.HTTP_400_BAD_REQUEST)
        # Tomo el turno que corresponde a ese id
        turno_taller = Turno_taller.objects.get(pk=id_turno)
        registro_evaluacion = Registro_evaluacion.objects.create(id_turno = turno_taller,
                                                                id_task_puntaje=id_task_puntaje, detalle=detalle)
        serializer = RegistroEvaluacionSerializer(registro_evaluacion)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@receiver(post_save, sender=Registro_evaluacion)
def generar_reporte_administracion(sender, instance, created, **kwargs):
    if created:
        detalle = instance.detalle
        puntaje_total = Checklist_evaluacion._meta.get_field('puntaje_max').default
        costo_total = 0.0
        duracion_total_reparaciones = 0

        turno = instance.id_turno
        id_task_puntaje = instance.id_task_puntaje  

        # calculo puntaje total
        for puntaje_seleccionado in id_task_puntaje.values():
            puntaje_total -= puntaje_seleccionado
        
        # calculo duracion total de las reparaciones y costo total
        for id_task in id_task_puntaje.keys():
            
            puntaje_seleccionado = id_task_puntaje.get(id_task)

            if puntaje_seleccionado > 0:

                task = Checklist_evaluacion.objects.get(id_task=id_task)
                duracion_reemplazo = task.duracion_reemplazo
                costo_reemplazo = task.costo_reemplazo

                duracion_total_reparaciones += duracion_reemplazo
                costo_total += costo_reemplazo
    
        reporte = Registro_evaluacion_para_admin(id_turno=turno, detalle=detalle,costo_total=costo_total,
                                                 duracion_total_reparaciones=duracion_total_reparaciones, puntaje_total=puntaje_total)
        
        reporte.save()
# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER TODOS------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if not Registro_evaluacion.objects.exists():
            return Response({'error': 'No hay registros actualmente'}, status=status.HTTP_204_NO_CONTENT)
        else:
            registros = Registro_evaluacion.objects.all()
            serializer = RegistroEvaluacionSerializer(registros, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER UNO--------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionUno(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_turno, format=None):
        if not Registro_evaluacion.objects.filter(id_turno=id_turno).exists():
             return Response({'error': 'No existen registros para el turno proporcionado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            registros = Registro_evaluacion.objects.filter(id_turno=id_turno)
            serializer = RegistroEvaluacionSerializer(registros, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER CON DETALLES-----------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionXAdminReadOnly(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if not Registro_evaluacion_para_admin.objects.exists():
            return Response({'error': 'No hay registros actualmente'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            registros = Registro_evaluacion_para_admin.objects.all()
            serializer = RegistroEvaluacionXAdminSerializerGET(registros, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
# -----------------------------------------------------------------------------------------------------
#------------------------------------CHECKLIST EVALUACION LEER-----------------------------------------
# -----------------------------------------------------------------------------------------------------
class ChecklistEvaluacionList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if not Checklist_evaluacion.objects.exists():
            return Response({'error': 'La checklist está vacía'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            checklist = Checklist_evaluacion.objects.all()
            serializer = ChecklistEvaluacionSerializer(checklist, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



