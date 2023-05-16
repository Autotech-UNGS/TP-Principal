import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



from administracion.models import  Turno_taller, Registro_evaluacion_para_admin, Registro_evaluacion, Checklist_evaluacion
from administracion.serializers import  RegistroEvaluacionXAdminSerializerGET, RegistroEvaluacionSerializer, ChecklistEvaluacionSerializer


# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION CREAR-----------------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionCreate(APIView):
    permission_classes = [permissions.AllowAny]
    
    # id_turno , diccionario ["id_task_puntaje":{"1":20, "2":30}], detalle 
    def post(self, request, *args, **kwargs):

        id_turno = request.data.get('id_turno')
        id_task_puntaje = request.data.get('id_task_puntaje')
        detalle = request.data.get('detalle')

        if Registro_evaluacion.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado ya existe en la base de datos'}, status=status.HTTP_400_BAD_REQUEST)
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
        puntaje_total = 2500
        costo_total = 0.0
        duracion_total_reparaciones = 0

        turno = instance.id_turno
        id_turno = turno.id_turno
        id_task_puntaje = instance.id_task_puntaje  

        # calculo puntaje total
        for puntaje_seleccionado in id_task_puntaje.values():
            puntaje_total -= puntaje_seleccionado
        
        # calculo duracion total de las reparaciones y costo total
        for id_task in id_task_puntaje.keys():
    
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
        registros = Registro_evaluacion.objects.all()
        serializer = RegistroEvaluacionSerializer(registros, many=True)
        return Response(serializer.data)

# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER UNO--------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionUno(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_turno, format=None):
        registros = Registro_evaluacion.objects.filter(id_turno=id_turno)
        serializer = RegistroEvaluacionSerializer(registros, many=True)
        return Response(serializer.data)

# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER CON DETALLES-----------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionXAdminReadOnly(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        registros = Registro_evaluacion_para_admin.objects.all()
        serializer = RegistroEvaluacionXAdminSerializerGET(registros, many=True)
        return Response(serializer.data)

    
# -----------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------
class ChecklistEvaluacionList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        checklist = Checklist_evaluacion.objects.all()
        serializer = ChecklistEvaluacionSerializer(checklist, many=True)
        return Response(serializer.data)


