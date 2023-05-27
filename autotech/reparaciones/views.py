import json
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.models import Turno_taller, Registro_reparacion, Registro_extraordinario, Registro_evaluacion, Registro_evaluacion_para_admin, Checklist_evaluacion
from administracion.serializers import ChecklistEvaluacionSerializer
from .validadores import ValidadorTurno, ValidadorRegistroReparacion


class RegistroReparacionViewSet(ViewSet):
    def registrar(self, turno, origen):
        validador_turno = ValidadorTurno()
        if not validador_turno.existe_turno(turno):
            return Response({'error': 'El turno no existe'}, status=status.HTTP_400_BAD_REQUEST)

        if not origen == 'extraordinario' and not  origen == 'evaluacion':
            return Response({'error': 'El turno no corresponde a un turno tipo extraordinario o un turno tipo evaluacion'}, status=status.HTTP_400_BAD_REQUEST)

        if origen == 'evaluacion':
            registro_evaluacion = self.obtener_registro_evaluacion(turno)

            if registro_evaluacion is None:
                return Response({'error': 'No existe registro de evaluación para la patente del turno'}, status=status.HTTP_400_BAD_REQUEST)

            tareas_con_puntaje_mayor_a_cero = self.filtrar_tareas_con_puntaje_mayor_a_cero(registro_evaluacion)

            registro_admin = Registro_evaluacion_para_admin.objects.get(id_turno=registro_evaluacion.id_turno)

            self.crear_registro_reparacion(turno, tareas_con_puntaje_mayor_a_cero, registro_admin.costo_total, registro_admin.duracion_total_reparaciones, origen, registro_evaluacion.detalle)

        if origen == 'extraordinario':
            registro_extraordinario = self.obtener_registro_extraordinario(turno)

            if registro_extraordinario is None:
                return Response({'error': 'No existe registro extraordinario para la patente del turno'}, status=status.HTTP_400_BAD_REQUEST)

            #tareas_registro = json.loads(registro_extraordinario.id_tasks)
            tareas_registro = registro_extraordinario.id_tasks
            detalle_evaluacion = registro_extraordinario.detalle
            costo_total, duracion_total = self.calcular_costo_y_duracion_total(tareas_registro)

            self.crear_registro_reparacion(turno, tareas_registro, costo_total, duracion_total, origen, detalle_evaluacion)

    def obtener_registro_evaluacion(self, turno):
        return Registro_evaluacion.objects.filter(id_turno__patente=turno.patente).last()

    def filtrar_tareas_con_puntaje_mayor_a_cero(self, registro_evaluacion):
        return [
            task_id
            for task_id, puntaje in registro_evaluacion.id_task_puntaje.items()
            if puntaje > 0
        ]

    def crear_registro_reparacion(self, turno, tasks_pendientes, costo_total, duracion_total, origen, detalle_evaluacion):
        Registro_reparacion.objects.create(
            id_turno=turno,
            tasks_pendientes=tasks_pendientes,
            costo_total=costo_total,
            duracion_total=duracion_total,
            origen=origen,
            detalle_evaluacion = detalle_evaluacion
        )

    def obtener_registro_extraordinario(self, turno):
        return Registro_extraordinario.objects.filter(id_turno__patente=turno.patente).first()

    def calcular_costo_y_duracion_total(self, tareas_registro):
        costo_total = 0.0
        duracion_total = 0

        for tarea_id in tareas_registro:
            checklist_evaluacion = Checklist_evaluacion.objects.get(id_task=tarea_id)
            costo_total += checklist_evaluacion.costo_reemplazo
            duracion_total += checklist_evaluacion.duracion_reemplazo

        return costo_total, duracion_total

    @action(detail=True, methods=['get'])
    def listar_tareas_registro_reparacion(self, request, id_turno):
        validador_registro = ValidadorRegistroReparacion()
        
        if not validador_registro.existe_registro_reparacion(id_turno):
            return Response({'error': f'No existe un registro de reparacion para el turno con id: {id_turno}'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not Checklist_evaluacion.objects.exists():
            return Response({'error': 'La checklist está vacía'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener el registro de reparacion perteneciente al turno
        registro_reparacion = Registro_reparacion.objects.get(id_turno=id_turno)
        tareas_hechas = registro_reparacion.tasks_hechas or []  # asignar una lista vacía si tasks_hechas es None
        tareas_pendientes = registro_reparacion.tasks_pendientes or []  # asignar una lista vacía si tasks_pendientes es None
        
        todas_tareas = tareas_hechas + tareas_pendientes
        
        # Filtrar las filas de checklist_evaluacion que contienen las tareas pendientes
        checklist = Checklist_evaluacion.objects.filter(id_task__in=todas_tareas)
        
        serializer = ChecklistEvaluacionSerializer(checklist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # id_turno , id_task, detalle
    @action(detail=False, methods=['patch'])
    def modificar_registro_tarea_hecha(self, request):
        id_turno = request.data.get('id_turno')
        id_task = request.data.get('id_task')
        detalle = request.data.get('detalle')

        if id_turno is None:
            return Response({'error': 'El campo "id_turno" es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        if id_task is None:
            return Response({'error': 'El campo "id_task" es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Obtenemos el registro de reparación perteneciente al turno
            turno = Turno_taller.objects.get(id_turno=id_turno)
            registro_reparacion = Registro_reparacion.objects.get(id_turno=turno)

            # Obtener las listas de tareas pendientes y tareas hechas
            tareas_pendientes = registro_reparacion.tasks_pendientes or []
            tareas_hechas = registro_reparacion.tasks_hechas or []

            # Comprobar si la tarea está en la lista de tareas pendientes
            if id_task not in tareas_hechas:
                # Comprobar si la tarea no está en la lista de tareas hechas
                if id_task in tareas_pendientes:
                    # Realizar las modificaciones necesarias
                    tareas_pendientes.remove(id_task)
                    tareas_hechas.append(id_task)
                    registro_reparacion.tasks_pendientes = tareas_pendientes
                    registro_reparacion.tasks_hechas = tareas_hechas
                    registro_reparacion.detalle = detalle
                    registro_reparacion.save()
                    return Response({'message': 'Registro modificado exitosamente'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'La tarea no corresponde a una tarea del registro'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'La tarea ya está en la lista de tareas hechas'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Turno_taller.DoesNotExist:
            return Response({'error': 'No se encontró un turno con el ID especificado'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Registro_reparacion.DoesNotExist:
            return Response({'error': 'No se encontró un registro de reparación para el turno especificado'}, status=status.HTTP_400_BAD_REQUEST)
    
    # id_turno , id_task, detalle
    @action(detail=False, methods=['patch'])
    def modificar_registro_tarea_pendiente(self, request):
        id_turno = request.data.get('id_turno')
        id_task = request.data.get('id_task')

        if id_turno is None:
            return Response({'error': 'El campo "id_turno" es requerido'}, status=status.HTTP_400_BAD_REQUEST)     
        if id_task is None:
            return Response({'error': 'El campo "id_task" es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Obtenemos el registro de reparación perteneciente al turno
            turno = Turno_taller.objects.get(id_turno=id_turno)
            registro_reparacion = Registro_reparacion.objects.get(id_turno=turno)

            # Obtener las listas de tareas pendientes y tareas hechas
            tareas_pendientes = registro_reparacion.tasks_pendientes or []
            tareas_hechas = registro_reparacion.tasks_hechas or []

            # Comprobar si la tarea no está en la lista de tareas pendientes
            if id_task not in tareas_pendientes:
                # Comprobar si la tarea está en la lista de tareas hechas
                if id_task in tareas_hechas:
                    # Realizar las modificaciones necesarias
                    tareas_hechas.remove(id_task)
                    registro_reparacion.tasks_hechas = tareas_hechas
                    registro_reparacion.save()
                    return Response({'message': 'Registro modificado exitosamente'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'La tarea no corresponde a una tarea del registro'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'La tarea ya está en la lista de tareas pendientes'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Turno_taller.DoesNotExist:
            return Response({'error': 'No se encontró un turno con el ID especificado'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Registro_reparacion.DoesNotExist:
            return Response({'error': 'No se encontró un registro de reparación para el turno especificado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def listar_tareas_registradas(self, request, id_turno):
        
        try:
            # Obtenemos el registro de reparación perteneciente al turno
            turno = Turno_taller.objects.get(id_turno=id_turno)
            registro_reparacion = Registro_reparacion.objects.get(id_turno=turno)
            tareas_pendientes = registro_reparacion.tasks_pendientes or []  # Obtener las tareas pendientes
            tareas_hechas = registro_reparacion.tasks_hechas or []  # Obtener las tareas hechas

            resultado = {}

            # Asignar valor False a las tareas pendientes
            for tarea_id in tareas_pendientes:
                resultado[str(tarea_id)] = False

            # Asignar valor True a las tareas hechas
            for tarea_id in tareas_hechas:
                resultado[str(tarea_id)] = True
         
            response = {
                "tasks": resultado,
                "detalle": registro_reparacion.detalle
            }
            return Response(response, status=status.HTTP_200_OK)   
        except Turno_taller.DoesNotExist:
            return Response({'error': 'No se encontró un turno con el ID especificado'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Registro_reparacion.DoesNotExist:
            return Response({'error': 'No se encontró un registro de reparación para el turno especificado'}, status=status.HTTP_400_BAD_REQUEST)
 

    @action(detail=True, methods=['get'])
    def mostrar_detalle_evaluacion_realizada(self, request, id_turno):
        try:
            # Obtenemos el registro de reparación perteneciente al turno
            turno = Turno_taller.objects.get(id_turno=id_turno)
            registro_reparacion = Registro_reparacion.objects.get(id_turno=turno)

            detalle = registro_reparacion.detalle_evaluacion
            return Response({"detalle_evaluacion": detalle}, status=status.HTTP_200_OK)
        except Turno_taller.DoesNotExist:
            return Response({'error': 'No se encontró un turno con el ID especificado'}, status=status.HTTP_400_BAD_REQUEST)
              
        except Registro_reparacion.DoesNotExist:
            return Response({'error': 'No se encontró un registro de reparación para el turno especificado'}, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=False, methods=['patch'])
    def modificar_detalle_reparacion(self, request):
        id_turno = request.data.get('id_turno')
        detalle = request.data.get('detalle')
        try:
            # Obtenemos el registro de reparación perteneciente al turno
            turno = Turno_taller.objects.get(id_turno=id_turno)
            registro_reparacion = Registro_reparacion.objects.get(id_turno=turno)

            registro_reparacion.detalle = detalle
            registro_reparacion.save()
            return Response({'message': 'detalle modificado exitosamente'}, status=status.HTTP_200_OK)
        except Turno_taller.DoesNotExist:
            return Response({'error': 'No se encontró un turno con el ID especificado'}, status=status.HTTP_400_BAD_REQUEST) 
              
        except Registro_reparacion.DoesNotExist:
            return Response({'error': 'No se encontró un registro de reparación para el turno especificado'}, status=status.HTTP_400_BAD_REQUEST)
        
    