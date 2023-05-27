from administracion.models import Taller, Service, Turno_taller, Registro_evaluacion_para_admin, Checklist_evaluacion, Registro_extraordinario, Registro_service
from datetime import date, time, timedelta
from math import ceil
import json

def obtener_email_usuario():
    #return 'forozco@campus.ungs.edu.ar'
    return 'luciacsoria5@gmail.com'
    
# cuando esta funciónn se invoca, ya sabemos que el taller existe    
def obtener_direccion_taller(taller_id) -> str:
    taller = Taller.objects.get(id_taller= taller_id)
    return f'{taller.direccion}, {taller.localidad}, {taller.provincia}.'

def obtener_duracion(fecha_inicio:date, hora_inicio:time, fecha_fin:date, hora_fin:time):
    if fecha_inicio == fecha_fin:
        return hora_fin.hour - hora_inicio.hour
    else:
        duracion = 0
        fecha = fecha_inicio
        hora = hora_inicio
        seguir = True
        while seguir:
            hora = time(hora.hour + 1, 0, 0)
            duracion += 1
            # si llegamos al dia y a la hora del fin del turno, terminamos el ciclo
            if fecha == fecha_fin and hora == hora_fin:
                seguir = False
            # si llegamos al final de la jornada, reiniciamos la hora y avanzamos un dia
            if (hora.hour == 17 and fecha.weekday() != 6) or (hora.hour == 12 and fecha.weekday() == 6):
                hora = time(8,0,0)
                fecha = fecha + timedelta(days=1)
    return duracion

def obtener_ultimo_service(patente:str):
    # tengo que encontrar todos los turnos de services de esa patente, y quedarme con el último
    # con ese ultimo turno de tipo service, tengo que encontrar el Registro_service que le corresponde
    # con el id_service de ese Registro_service, tengo que encontrar el Service correspondiente
    # con ese Service, obtengo la frecuencia_km, y la retorno
    ultimo_turno_service = Turno_taller.objects.filter(patente=patente, tipo='service').latest('fecha_inicio')
    registro_de_ultimo_service = Registro_service.objects.get(id_turno=ultimo_turno_service.id_turno)
    ultimo_service = Service.objects.get(id_service=registro_de_ultimo_service.id_service.id_service)
    
    return ultimo_service.frecuencia_km


def obtener_fecha_hora_fin(dia_inicio:date, horario_inicio:time, duracion:int) -> list: #[fecha_fin, hora_fin]
    fin_horario_de_trabajo = 17
    fin_horario_de_trabajo_domingos = 12
    
    fecha_hora_fin = []
    hora = horario_inicio.hour
    fecha = dia_inicio
    for i in range(duracion):
        if (hora == fin_horario_de_trabajo and fecha.weekday() != 6) or (hora == fin_horario_de_trabajo_domingos and fecha.weekday() == 6):
            hora = 8
            fecha = fecha + timedelta(days=1)
        hora += 1
        
    fecha_hora_fin.append(fecha)
    fecha_hora_fin.append(time(hora,0,0))
    
    return fecha_hora_fin

# retorna -1 si el service no existe
def obtener_duracion_service(marca:str, modelo:str, km:int):
    try:
        service = Service.objects.get(marca=marca, modelo=modelo, frecuencia_km=km)
        return ceil(service.duracion_total / 60)
    except:
        return -1

# viene de venta        
# retorna -1 si no existe un turno para evaluacion para esa patente
def obtener_duracion_reparacion(patente:str): 
    try:
        # 1) obtenemos el turno para evaluacion correspondiente a la reparacion que queremos hacer
        turno = Turno_taller.objects.filter(patente=patente, tipo= 'evaluacion').latest('fecha_inicio')
       
        # 2) con ese turno, nos traemos el turno para admin correspondiente, el cual tiene la duracion que necesitamos
        registro_admin = Registro_evaluacion_para_admin.objects.get(id_turno=turno.id_turno)
        return ceil(registro_admin.duracion_total_reparaciones / 60)
    except:
        return -1
    
# viene de extraordinario    
# retorna -1 si no existe un turno para evaluacion para esa patente
def obtener_duracion_extraordinario(patente:str):
    try:
        # 1) obtenemos el turno para evaluacion correspondiente a la reparacion que queremos hacer
        turno = Turno_taller.objects.filter(patente=patente, tipo= 'extraordinario').latest('fecha_inicio')
        # 2) con ese turno, nos traemos el registro_extraordinario correspondiente
        registro_extraordinario = Registro_extraordinario.objects.get(id_turno=turno.id_turno)
        # 3) con ese registro, ya tenemos las tareas que deben realizarse
        lista_task = json.loads(registro_extraordinario.id_tasks)
        #lista_task = registro_extraordinario.id_tasks
        # 4) recorremos los task para obtener el tiempo de cada uno
        duracion = 0
        for id in lista_task:
            item = Checklist_evaluacion.objects.get(id_task = id)
            duracion += item.duracion_reemplazo
        return ceil(duracion / 60) 
    except:
        return -1

