#import requests
from administracion.models import Turno_taller
from datetime import date, time
from .gestion_agenda.gestionar_agenda import *
from empleados.api_client.client_tecnico import ClientTecnicos

# -------- dias y horarios disponibles -------- #
def dias_horarios_disponibles_treinta_dias(id_taller:int, cant_horas:int):
    return dias_disponibles_desde_hoy_a_treinta_dias(id_taller, cant_horas)

def dias_horarios_disponibles_cuarentaycinco_dias(id_taller, cant_horas:int):
    return dias_disponibles_desde_hoy_a_cuarentaycinco_dias(id_taller, cant_horas)

def existe_taller(taller_id:int):
        try:
            taller = Taller.objects.get(id_taller= taller_id)
        except:
            return False
        else:
            return True

# -------- tecnicos disponibles -------- #

# devuelve una lista con los id de los tecnicos que podrían encargarse del turno
def obtener_tecnicos_disponibles(id_turno: int, id_taller: int) -> list:
    tecnicos_disponibles = []
    id_tecnicos = obtener_id_tecnicos(id_taller)    # sólo consideramos los tecnicos que trabajan en ese taller
    turno = Turno_taller.objects.get(id_turno=id_turno) # obtenemos el turno en cuestion, porque necesitamos sus horarios
    for id_tecnico in id_tecnicos:
        # esta disponible ==  tiene ese espacio disponible en su agenda, sin contar turnos terminados/cancelados/rechazados
        if tecnico_esta_disponible_agenda(turno.fecha_inicio, turno.hora_inicio, turno.fecha_fin, turno.hora_fin, id_tecnico):
            tecnicos_disponibles.append(id_tecnico)
    return tecnicos_disponibles

def obtener_id_tecnicos(id_taller: int) -> list:
    tecnicos = ClientTecnicos.obtener_datos_especificos_tecnicos(f'T00{id_taller}')
    id_tecnicos = []
    for tecnico in tecnicos:
        id_tecnicos.append(tecnico['id'])
    return id_tecnicos

# -------- asignar tecnico -------- #
    
def se_puede_asignar_tecnico(tipo_turno: str, papeles_en_regla_turno: bool):
    if tipo_turno != "evaluacion":
        es_valido = True
    elif papeles_en_regla_turno == True: # si el estado es rechazado, los papeles estan en False
        es_valido = True
    else:
        es_valido = False
    return es_valido

def tecnico_esta_disponible(id_tecnico: int, fecha_inicio:date, hora_inicio:time, fecha_fin:date, hora_fin:time):
    return tecnico_esta_disponible_agenda(fecha_inicio, hora_inicio, fecha_fin, hora_fin, id_tecnico)

def coinciden_los_talleres(id_tecnico: int, id_taller: int):
    taller_del_tecnico = obtener_taller_del_tecnico(id_tecnico)
    return int(taller_del_tecnico[-3:]) == id_taller

def obtener_taller_del_tecnico(id_tecnico):
    return ClientTecnicos.obtener_taller_tecnico(id_tecnico)