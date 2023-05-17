from rest_framework.exceptions import ValidationError
from administracion.models import Checklist_evaluacion


class ValidadorChecklist:

    def validar_diccionario(self, request):

        id_task_puntaje = request.data.get('id_task_puntaje')
        filas_checklist = Checklist_evaluacion.objects.count()
        print(filas_checklist, len(id_task_puntaje))
        if filas_checklist == len(id_task_puntaje):
            for id_task, puntaje_seleccionado  in id_task_puntaje.items():
                print(id_task)
                task = Checklist_evaluacion.objects.get(id_task = id_task)
                puntaje_maximo_item = task.puntaje_max

                if puntaje_seleccionado is None:
                     raise ValidationError(f'No se ha seleccionado un valor para la tarea {id_task}: {task.elemento}')
                
                if puntaje_seleccionado < 0:
                    raise ValidationError(f'Las tareas no pueden tener puntajes negativos. Revisar la tarea {id_task}: {task.elemento}')

                if puntaje_seleccionado > puntaje_maximo_item:
                    raise ValidationError(f'La tarea {id_task}: {task.elemento} supera el puntaje máximo de la misma: {puntaje_maximo_item}')
        else:
             raise ValidationError(f'Faltan tareas por calificar')
        return True
