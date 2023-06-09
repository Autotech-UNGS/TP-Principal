import json
from rest_framework.exceptions import ValidationError
from administracion.models import Checklist_evaluacion
from rest_framework import status
from rest_framework.response import Response


class ValidadorChecklist:

    def validar_diccionario(self, request):
        id_task_puntaje = request.data.get('id_task_puntaje')
        if not id_task_puntaje:
            return Response({'error': 'El campo "id_task_puntaje" es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        filas_checklist = Checklist_evaluacion.objects.count()
        if filas_checklist == len(id_task_puntaje):  # comparo que la lista que me llega de tasks sea igual a las filas_checklist de la tabla checklist_Evaluación predefinida en la BD
           
            for id_task, puntaje_seleccionado  in id_task_puntaje.items():  # por cada fila obtengo la tarea y el puntaje 
                
                 # obtengo la informacion del id de la tarea
                if not Checklist_evaluacion.objects.filter(id_task=id_task).exists():
                     raise ValidationError(f'No existe una tarea con el id: {id_task}') 
                 
                task = Checklist_evaluacion.objects.get(id_task=id_task)
                puntaje_maximo_item = task.puntaje_max #obtengo el puntaje maximo de esa tarea

                if puntaje_seleccionado is None:
                     raise ValidationError(f'No se ha seleccionado un valor para la tarea {id_task}: {task.elemento}')  # si el puntaje que tengo es vacio se tiene que tirar un erro
                
                elif puntaje_seleccionado < 0:
                    raise ValidationError(f'Las tareas no pueden tener puntajes negativos. Revisar la tarea {id_task}: {task.elemento}')

                elif puntaje_seleccionado > puntaje_maximo_item:
                    raise ValidationError(f'La tarea {id_task}: {task.elemento} supera el puntaje máximo de la misma: {puntaje_maximo_item}')
        else:
             raise ValidationError(f'Faltan tareas por calificar')
        return True

    def validar_tareas(self, request):
        id_tasks = request.data.get('id_tasks')
        
        if not id_tasks:
            return Response({'error': 'El campo "id_tasks" es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        id_tasks = json.loads(id_tasks)  # Convertir id_tasks de cadena de texto JSON a lista de enteros
        
        id_task_evaluacion= Checklist_evaluacion.objects.values_list('id_task', flat=True)
        if not set(id_tasks).issubset(id_task_evaluacion):
             raise ValidationError(f'Existen tareas de {id_tasks} que no están incluidas en la checklist de evaluacion')
        
        return True