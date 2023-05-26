from administracion.models import Taller, Service, Turno_taller, Registro_reparacion, Registro_evaluacion, Checklist_evaluacion
from datetime import date, time, timedelta

def obtener_email_usuario():
    #return 'forozco@campus.ungs.edu.ar'
    return 'luciacsoria5@gmail.com'
    
def obtener_direccion_taller(taller_id) -> str:
    taller = Taller.objects.get(id_taller= taller_id)
    return f'{taller.direccion}, {taller.localidad}, {taller.provincia}.'

def obtener_fecha_hora_fin(dia_inicio:date, horario_inicio:time, duracion:int) -> list: #[fecha_fin, hora_fin]
    fin_horario_de_trabajo = 17
    fin_horario_de_trabajo_domingos = 12
    
    fecha_hora_fin = []
    hora = horario_inicio
    fecha = dia_inicio
    for i in range(duracion):
        if (hora == fin_horario_de_trabajo and fecha.weekday() != 6) or (hora == fin_horario_de_trabajo_domingos and fecha.weekday() == 6):
            hora = 8
            fecha = fecha + timedelta(days=1)
        hora+=1
        
    fecha_hora_fin.append(fecha)
    fecha_hora_fin.append(hora)
    
    return fecha_hora_fin

def obtener_duracion_service(marca:str, modelo:str, km:int):
    service = Service.objects.get(marca=marca, modelo=modelo, frecuencia_km=km)
    return service.duracion_total

# viene de venta        
def obtener_duracion_reparacion(patente:str): 
    turno = Turno_taller.objects.filter(patente=patente, tipo= 'evaluacion').latest('fecha_inicio')
    id_turno = turno.id_turno
    registros_evaluacion = Registro_evaluacion.objects.filter(id_turno=id_turno)
    duracion = 0
    for registro in registros_evaluacion:
        id_task_puntaje = registro.id_task_puntaje  
        for id_task in id_task_puntaje.keys():            
            puntaje_seleccionado = id_task_puntaje.get(id_task)
            if puntaje_seleccionado > 0:
                task = Checklist_evaluacion.objects.get(id_task=id_task)
                duracion += task.duracion_reemplazo
    return duracion
    
# viene de extraordinario    
def obtener_duracion_extraordinario(patente:str):
    return 0
"""
    turno = Turno_taller.objects.filter(patente=patente, tipo= 'extraordinario').latest('fecha_inicio')
    id_turno = turno.id_turno
    registros_extraordinario = Registro_extraordinario.objects.filter(id_turno=id_turno)
    duracion = 0
    for registro in registros_extraordinario:
        id_task_puntaje = registro.id_task_puntaje  
        for id_task in id_task_puntaje.keys():            
            puntaje_seleccionado = id_task_puntaje.get(id_task)
            if puntaje_seleccionado > 0:
                task = Checklist_extraordinario.objects.get(id_task=id_task) # o es la misma que evaluacion?
                duracion += task.duracion_reemplazo
    return duracion
    """
        
