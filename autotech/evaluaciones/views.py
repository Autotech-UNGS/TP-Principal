import json
import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.decorators import action

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from administracion.models import  Turno_taller, Registro_evaluacion_para_admin, Registro_evaluacion, Checklist_evaluacion, Registro_extraordinario
from administracion.serializers import  RegistroEvaluacionXAdminSerializer, RegistroEvaluacionSerializer, ChecklistEvaluacionSerializer, TurnoTallerSerializer, RegistroExtraordinarioSerializer
from .validadores import ValidadorChecklist



# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION CREAR-----------------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionCreate(APIView):
    permission_classes = [permissions.AllowAny]
    
    # id_turno , diccionario ["id_task_puntaje":{"1":20, "2":30}], detalle 
    def post(self, request, *args, **kwargs):
        validador = ValidadorChecklist()
        detalle = request.data.get('detalle')

        id_turno = request.data.get('id_turno')
        if not id_turno:
            return Response({'error': 'El campo "id_turno" es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        if not Turno_taller.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        turno = Turno_taller.objects.get(id_turno=id_turno)

        if not turno.tipo == "evaluacion":
            return Response({'error': 'El turno pasado no es un turno para Evaluación'}, status=status.HTTP_400_BAD_REQUEST)
    
        if not turno.estado == "en_proceso":
            return Response({'error': 'El turno pasado no está en estado en proceso'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validador.validar_diccionario(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
        
        id_task_puntaje = request.data.get('id_task_puntaje')

        

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

        # ----------------------- ARREGLO INTEGRACION GRUPO 4 ----------------------------------------------------------- #
        checklist = Checklist_evaluacion.objects.all()
        turno_instancia = Turno_taller.objects.get(id_turno = reporte.id_turno.id_turno)
        patente = turno_instancia.patente
        puntaje_maximo_tasks = 0
        for registro in checklist:
            puntaje_maximo_tasks += registro.puntaje_max

        """ print(f'puntaje total: {reporte.puntaje_total}')
        print(f'puntaje maximo tareas: {puntaje_maximo_tasks}') """

        porcentaje = ((reporte.puntaje_total*100)/puntaje_maximo_tasks)
        """ print(f'porcentaje: {porcentaje}') """


        url = 'https://gadmin-backend-production.up.railway.app/api/v1/vehicle/saveTechInfo'
        data = {
                "plate": patente,
                "score": porcentaje,
                "repairCost":reporte.costo_total,
                "message": reporte.detalle
                }  # Datos adicionales que quieras enviar en el post
        #print(data)
        
        try:
            response = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            #print('¡Registro enviado existosamente!', response.status_code)
        except requests.exceptions.RequestException as e:
            print('Ocurrió un error al enviar el registro a administración:', str(e))


# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER TODOS------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if not Registro_evaluacion.objects.exists():
            return Response({'message': 'No hay registros actualmente'}, status=status.HTTP_204_NO_CONTENT)
        else:
            registros = Registro_evaluacion.objects.all()
            serializer = RegistroEvaluacionSerializer(registros, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER UNO--------------------------------------
# -----------------------------------------------------------------------------------------------------
""" class RegistroEvaluacionUno(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_turno, format=None):
        import pdb; pdb.set_trace()
        if not Registro_evaluacion.objects.filter(id_turno=id_turno).exists():
             return Response({'error': 'No existen registros para el turno proporcionado'}, status=status.HTTP_404_NOT_FOUND)
        else:
            registros = Registro_evaluacion.objects.filter(id_turno=id_turno)
            serializer = RegistroEvaluacionSerializer(registros, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
 """
# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER CON DETALLES-----------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionXAdminReadOnly(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if not Registro_evaluacion_para_admin.objects.exists():
            return Response({'message': 'No hay registros actualmente'}, status=status.HTTP_204_BAD_REQUEST)
        else:
            registros = Registro_evaluacion_para_admin.objects.all()
            serializer = RegistroEvaluacionXAdminSerializer(registros, many=True)
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


# -----------------------------------------------------------------------------------------------------
#------------------------REGISTRO EVALUACION LEER PARA UN TECNICO CON DETALLES-------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionXAdminReadOnlyTecnico(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_tecnico, format=None):

        # No hay registros de evaluación
        if not Registro_evaluacion_para_admin.objects.exists():
            return Response({'error': 'No hay registros actualmente'}, status=status.HTTP_204_NO_CONTENT)
        
        # El técnico pasado no tiene turnos de evaluacionen proceso actualmente 
        if not Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='evaluacion'):
            return Response({'error': 'El ID del técnico no es válido con un turno de evaluación vigente'}, status=status.HTTP_400_BAD_REQUEST)
        
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='evaluacion')
        id_turnos = list(turnos.values_list('id_turno', flat=True))

        # El técnico no tiene registros de evaluación guardados
        if not Registro_evaluacion_para_admin.objects.filter(id_turno__in = id_turnos):
            return Response({'error': 'El Técnico no posee registros de evaluación guardados'}, status=status.HTTP_400_BAD_REQUEST)
        
        registros = Registro_evaluacion_para_admin.objects.filter(id_turno__in = id_turnos)    
        serializer = RegistroEvaluacionXAdminSerializer(registros, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER PARA UN TECNICO -------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionListTecnico(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_tecnico, format=None):
        
        # El técnico pasado no tiene turnos de evaluacionen proceso actualmente 
        """  if not Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='evaluacion'):
            return Response({'error': 'El ID del técnico no es válido con un turno de evaluación vigente'}, status=status.HTTP_400_BAD_REQUEST) """
        
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='evaluacion')
        id_turnos = list(turnos.values_list('id_turno', flat=True))

        # El técnico no tiene registros de evaluación guardados
        if not Registro_evaluacion.objects.filter(id_turno__in = id_turnos):
            serializer = TurnoTallerSerializer(turnos, many=True)
            # Si no tiene turnos registrados de evalaucion entonces devuelvo todos los turnos que tenga 
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        registros = Registro_evaluacion.objects.filter(id_turno__in = id_turnos) 
        id_turnos_registros = list(registros.values_list('id_turno', flat=True))

        turnos_pendientes_de_registro = Turno_taller.objects.filter(id_turno__in = id_turnos).exclude(id_turno__in = id_turnos_registros)
        serializer = TurnoTallerSerializer(turnos_pendientes_de_registro, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    

# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EXTRAORDINARIO CREAR -------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroExtraordinarioCreate(APIView):
    permission_classes = [permissions.AllowAny]
    
    # id_turno, "id_tasks":"[1,2,3,4,5]", detalle
    def post(self, request, *args, **kwargs):
        validador = ValidadorChecklist()
        id_turno = request.data.get('id_turno')
        id_tasks = request.data.get('id_tasks')
        detalle = request.data.get('detalle')

        if not id_turno:
            return Response({'error': 'El campo "id_turno" es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        if not Turno_taller.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        turno = Turno_taller.objects.get(id_turno=id_turno)

        if not turno.tipo == 'extraordinario':
            return Response({'error': 'El turno pasado no es un turno para extraordinario'}, status=status.HTTP_400_BAD_REQUEST)
    
        if not turno.estado == 'en_proceso':
            return Response({'error': 'El turno pasado no está en estado en proceso'}, status=status.HTTP_400_BAD_REQUEST)   
        
        if not turno.estado == 'en_proceso':
            return Response({'error': 'El turno pasado no está en estado en proceso'}, status=status.HTTP_400_BAD_REQUEST)   
        
        try:
            id_tasks = json.loads(id_tasks)  # Convertir id_tasks a lista
            id_tasks = [str(task_id) for task_id in id_tasks]  # Convertir los IDs de tareas a cadenas de texto
            validador.validar_tareas(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST)

        # Tomo el turno que corresponde a ese id
        turno_taller = Turno_taller.objects.get(pk=id_turno)

        # Verificar si ya existe un registro extraordinario para el turno
        if Registro_extraordinario.objects.filter(id_turno=turno_taller).exists():
            return Response({'error': 'Ya existe un registro extraordinario para este turno'}, status=status.HTTP_400_BAD_REQUEST)
        
        registro_extraordinario = Registro_extraordinario.objects.create(id_turno = turno_taller,
                                                                id_tasks=id_tasks, detalle=detalle)
        serializer = RegistroExtraordinarioSerializer(registro_extraordinario)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class RegistroExtraordinarioListTecnico(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_tecnico, format=None):
        
        # El técnico pasado no tiene turnos de evaluacionen proceso actualmente 
        """  if not Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='evaluacion'):
            return Response({'error': 'El ID del técnico no es válido con un turno de evaluación vigente'}, status=status.HTTP_400_BAD_REQUEST) """
        
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='extraordinario')
        id_turnos = list(turnos.values_list('id_turno', flat=True))

        # El técnico no tiene registros extraordinarios guardados
        if not Registro_extraordinario.objects.filter(id_turno__in = id_turnos):
            serializer = TurnoTallerSerializer(turnos, many=True)
            # Si no tiene turnos registrados extraordinario entonces devuelvo todos los turnos que tenga 
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        registros = Registro_extraordinario.objects.filter(id_turno__in = id_turnos) 
        id_turnos_registros = list(registros.values_list('id_turno', flat=True))

        turnos_pendientes_de_registro = Turno_taller.objects.filter(id_turno__in = id_turnos).exclude(id_turno__in = id_turnos_registros)
        serializer = TurnoTallerSerializer(turnos_pendientes_de_registro, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
