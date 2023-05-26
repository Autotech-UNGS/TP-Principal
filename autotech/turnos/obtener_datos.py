from administracion.models import Taller, Service, Turno_taller, Registro_evaluacion_para_admin
from datetime import date, time, timedelta

def obtener_email_usuario():
    #return 'forozco@campus.ungs.edu.ar'
    return 'luciacsoria5@gmail.com'
    
# cuando esta funciónn se invoca, ya sabemos que el taller existe    
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

# retorna -1 si el service no existe
def obtener_duracion_service(marca:str, modelo:str, km:int):
    try:
        service = Service.objects.get(marca=marca, modelo=modelo, frecuencia_km=km)
        return service.duracion_total
    except:
        return -1

# viene de venta        
# retorna -1 si no existe un turno para evaluacion para esa patente
def obtener_duracion_reparacion(patente:str): 
    try:
        # 1) obtenemos el turno para evaluacion correspondiente a la reparacion que queremos hacer
        turno = Turno_taller.objects.filter(patente=patente, tipo= 'evaluacion').latest('fecha_inicio')
        # 2) con ese turno, nos traemos el turno para admin correspondiente, el cual tiene la duracion que necesitamos
        registro_admin = Registro_evaluacion_para_admin.objects.get(id_turno=turno)
        return registro_admin.duracion_total_reparaciones
    except:
        return -1
    
# viene de extraordinario    
# retorna -1 si no existe un turno para evaluacion para esa patente
def obtener_duracion_extraordinario(patente:str):
    return 0
"""

    # 1) obtenemos el turno para evaluacion correspondiente a la reparacion que queremos hacer
    turno = Turno_taller.objects.filter(patente=patente, tipo= 'evaluacion', origen='extraordinario').latest('fecha_inicio')
    id_turno = turno.id_turno
    # 2) con el id de ese turno, nos traemos el turno para admin correspondiente, el cual tiene la duracion que necesitamos
    registro_admin = Registro_evaluacion_para_admin.objects.get(id_turno=id_turno)
    return registro_admin.duracion_total_reparaciones
    
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
        
