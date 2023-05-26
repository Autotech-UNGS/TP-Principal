from rest_framework.exceptions import ValidationError
from administracion.models import Service

class ValidadorService:
    #marca, modelo, frecuencia_km, costo_base, id_supervisor
    def validar_service(self, request):
         marca = request.data.get('marca')
         modelo = request.data.get('modelo')
         frecuencia_km = request.data.get('frecuencia_km')
         costo_base = request.data.get('costo_base')
         id_supervisor = request.data.get('id_supervisor')

         pass


        





""" id_task_puntaje = request.data.get('id_task_puntaje')
        filas_checklist = Checklist_evaluacion.objects.count()
        if filas_checklist == len(id_task_puntaje):
            for id_task, puntaje_seleccionado  in id_task_puntaje.items():

                task = Checklist_evaluacion.objects.get(id_task = id_task)
                puntaje_maximo_item = task.puntaje_max

                if puntaje_seleccionado is None:
                     raise ValidationError(f'No se ha seleccionado un valor para la tarea {id_task}: {task.elemento}')
                
                elif puntaje_seleccionado < 0:
                    raise ValidationError(f'Las tareas no pueden tener puntajes negativos. Revisar la tarea {id_task}: {task.elemento}')

                elif puntaje_seleccionado > puntaje_maximo_item:
                    raise ValidationError(f'La tarea {id_task}: {task.elemento} supera el puntaje máximo de la misma: {puntaje_maximo_item}')
        else:
             raise ValidationError(f'Faltan tareas por calificar')
        return True """