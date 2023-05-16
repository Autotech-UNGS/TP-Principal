#import requests
from administracion.models import Turno_taller
from datetime import date, time
from .gestion_agenda.gestionar_agenda import *
from tecnicos.views import *
from tecnicos.consumidor_api_externa import ConsumidorApiTecnicos

# -------- dias y horarios disponibles -------- #
def dias_horarios_disponibles_treinta_dias(id_taller:int):
    return dias_disponibles_desde_hoy_a_treinta_dias(id_taller)

# -------- crear turno -------- #

def horarios_exactos(hora_inicio:time, hora_fin:time):
    return hora_inicio.minute == 0 and hora_fin.minute == 0 and hora_inicio.second == 0 and hora_fin.second == 0 # and hora_inicio <= hora_fin
        
def horarios_dentro_de_rango(dia:date, horario_inicio:time, horario_fin:time):
    horario_valido = horario_inicio < horario_fin
    if dia.weekday() == 6: # domigo
        horario_inicio_valido = horario_inicio.hour >= 8 and horario_inicio.hour <= 11 # podemos dar turnos de 8 a 11
        horario_fin_valido = horario_fin.hour >= 9 and horario_fin.hour <= 12 # los turnos pueden terminar de 9 a 12
    else:
        horario_inicio_valido = horario_inicio.hour >= 8 and horario_inicio.hour <= 16 # podemos dar turnos de 8 a 16
        horario_fin_valido = horario_fin.hour >= 9 and horario_fin.hour <= 17 # los turnos pueden terminar de 9 a 17
    return horario_inicio_valido and horario_fin_valido and horario_valido
    
def dia_hora_coherentes(dia_inicio: date, horario_inicio: time, dia_fin: date , horario_fin: time):
    if dia_inicio < dia_fin:
        es_valido = True
    elif dia_inicio == dia_fin:
        es_valido = horario_inicio < horario_fin
    else:
        es_valido = False
    return es_valido
    
def dia_valido(dia: date):
    return dia > date.today()

# -------- tecnicos disponibles -------- #

# devuelve una lista con los id de los tecnicos que podrían encargarse del turno
def obtener_tecnicos_disponibles(id_turno: int, id_taller: int) -> list:
    tecnicos_disponibles = []
    id_tecnicos = obtener_id_tecnicos(id_taller)    # sólo consideramos los tecnicos que trabajan en ese taller
    turno = Turno_taller.objects.get(id_turno=id_turno) # obtenemos el turno en cuestion, porque necesitamos sus horarios
    for id_tecnico in id_tecnicos:
        # esta disponible ==  tiene ese espacio disponible en su agenda, sin contar turnos terminados/cancelados/rechazados
        if esta_disponible(id_tecnico, turno.fecha_inicio, turno.hora_inicio, turno.fecha_fin, turno.hora_fin):
            tecnicos_disponibles.append(id_tecnico)
    return tecnicos_disponibles

def obtener_id_tecnicos(id_taller: int) -> list:
    tecnicos = ConsumidorApiTecnicos.consumir_tecnicos(f'S00{id_taller}')
    id_tecnicos = []
    for tecnico in tecnicos:
        id_tecnicos.append(tecnico['id_empleado'])
    return id_tecnicos

# -------- asignar tecnico -------- #
    
def se_puede_asignar_tecnico(tipo_turno: str, papeles_en_regla_turno: bool):
    if tipo_turno != "evaluacion":
        es_valido = True
    elif papeles_en_regla_turno == True:
        es_valido = True
    else:
        es_valido = False
    return es_valido

def esta_disponible(id_tecnico: int, fecha_inicio:date, hora_inicio:time, fecha_fin:date, hora_fin:time):
    return tecnico_esta_disponible(fecha_inicio, hora_inicio, fecha_fin, hora_fin, id_tecnico)

def coinciden_los_talleres(id_tecnico: int, id_taller: int):
    taller_del_tecnico = obtener_taller_del_tecnico(id_tecnico)
    return int(taller_del_tecnico[-1]) == id_taller

def obtener_taller_del_tecnico(id_tecnico):
    return ConsumidorApiTecnicos.obtener_taller_tecnico(id_tecnico)

class ValidadorSupervisor():

    def sucursal(self, sucursal_supervisor):
        if sucursal_supervisor is None:
            return False
        if len(sucursal_supervisor) != 4:
            return False
        if sucursal_supervisor[0] != 'S':
            return False
        if not sucursal_supervisor[1:].isdigit():
            return False   
        return True
