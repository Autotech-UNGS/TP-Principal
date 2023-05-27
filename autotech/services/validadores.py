from rest_framework.exceptions import ValidationError
from administracion.models import Checklist_service, Service
from administracion.validadores import Frecuencia_km
# from empleados.api_client.client_supervisor import ClientSupervisor

class ValidadorService:
    checklist_service = Checklist_service.objects.all()
#marca, modelo, frecuencia_km, costo_base, id_supervisor
    def validar_service(self, request):
        marca = (request.data.get('marca')).lower()
        modelo = (request.data.get('modelo')).lower()
        frecuencia_km = request.data.get('frecuencia_km')
        costo_base = request.data.get('costo_base')
        id_supervisor = request.data.get('id_supervisor')
        id_tasks = request.data.get('id_tasks')

        if id_tasks == "[]" or not id_tasks:
             raise ValidationError('no se están pasando tareas para agregar al service')

        if marca is None:
             raise ValidationError(f'El campo marca está vacio o no fue pasado')
        if modelo is None:
             raise ValidationError(f'El campo modelo está vacio o no fue pasado')
        if frecuencia_km is None:
             raise ValidationError(f'El campo frecuencia_km está vacio o no fue pasado')
        if costo_base is None:
             raise ValidationError(f'El campo costo_base está vacio o no fue pasado')
        if id_supervisor is None:
             raise ValidationError(f'El campo id_supervisor está vacio o no fue pasado')
        
        if frecuencia_km not in [choice[0] for choice in Frecuencia_km.choices]:
             raise ValidationError(f'La frecuencia de kilometraje {frecuencia_km} no está entre las frecuencias trabajadas. 5000 a 200000, con saltos de 5000 en 5000')
        
        if costo_base < 0:
             raise ValidationError(f'El campo {str(costo_base)} no puede ser un valor negativo')
        
        existing_service = Service.objects.filter(marca=marca, modelo=modelo, frecuencia_km=frecuencia_km).exists()
        if existing_service:
             raise ValidationError(f'Ya se encuenta un service registrado para la marca: {marca} y modelo: {modelo} para {frecuencia_km} KM')
        
        # Validar si el supervisor existe en la tabla de usuarios
        """ if not ClientSupervisor.existe_supervisor(id_supervisor):
             raise ValidationError(f'El id {id_supervisor} no es válido a un supervisor o no existe') """
        
        return True
    
    def validar_tareas(self, id_tasks):
        cant_tareas_service = self.checklist_service.count()
        
        if len(id_tasks) > cant_tareas_service:
             raise ValidationError(f'Se están ingresando {len(id_tasks)} y solo están registradas {cant_tareas_service} tareas.')
        
        id_tareas_service = Checklist_service.objects.values_list('id_task', flat=True)
        if not set(id_tasks).issubset(id_tareas_service):
             raise ValidationError(f'Existen tareas de {id_tasks} que no están incluidas en la checklist de service')
        
        return True

        





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