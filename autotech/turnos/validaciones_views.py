#import requests
from administracion.models import Turno_taller
from datetime import date, time
from .gestion_agenda.gestionar_agenda import *

# -------- crear turno -------- #

def horarios_exactos(hora_inicio:time, hora_fin:time):
    return hora_inicio.minute == 0 and hora_fin.minute == 0 and hora_inicio.second == 0 and hora_fin.second == 0 # and hora_inicio <= hora_fin
        
def horarios_dentro_de_rango(dia:date, horario_inicio:time, horario_fin:time):
    if dia.weekday() == 6: # domigo
        horario_inicio_valido = horario_inicio.hour >= 8 and horario_inicio.hour <= 11 # podemos dar turnos de 8 a 11
        horario_fin_valido = horario_fin.hour >= 9 and horario_fin.hour <= 12 # los turnos pueden terminar de 9 a 12
    else:
        horario_inicio_valido = horario_inicio.hour >= 8 and horario_inicio.hour <= 16 # podemos dar turnos de 8 a 16
        horario_fin_valido = horario_fin.hour >= 9 and horario_fin.hour <= 17 # los turnos pueden terminar de 9 a 17
    return horario_inicio_valido and horario_fin_valido
    
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

# -------- asignar tecnico -------- #
    
def se_puede_asignar_tecnico(tipo_turno: str, papeles_en_regla_turno: bool):
    if tipo_turno != "Evaluacion":
        es_valido = True
    elif papeles_en_regla_turno == True:
        es_valido = True
    else:
        es_valido = False
    return es_valido

def esta_disponible(id_tecnico: int, fecha_inicio:date, hora_inicio:time, fecha_fin:date, hora_fin:time):
    return tecnico_esta_disponible(fecha_inicio, hora_inicio, fecha_fin, hora_fin, id_tecnico)

"""
def esta_disponible(id_tecnico: int, dia:date, hora_inicio:time, hora_fin:time):
    # Si el id del tecnico no aparece en ningun turno, da una excepcion. Para evitarlo, hacemos
    # retornamos True --> no tiene turnos, entonces esta disponible
    try:
        turnos_del_tecnico = Turno_taller.objects.filter(tecnico_id = id_tecnico).filter(fecha_inicio = dia)
    except:
    #if turnos_del_tecnico == None:
        return True
    else:
        #print(Turno_taller.objects.all())
        turnos_del_tecnico = Turno_taller.objects.filter(tecnico_id = id_tecnico).filter(fecha_inicio = dia)
        esta_disponible = True
        for turno in turnos_del_tecnico:
            esta_disponible = esta_disponible and no_hay_superposicion(turno.hora_inicio, turno.hora_fin, hora_inicio, hora_fin)
        
        return esta_disponible
            
def no_hay_superposicion(hora_inicio1: time, hora_fin1: time, hora_inicio2: time, hora_fin2: time):
    resultado = True
    # comienzan o terminan a la vez
    if hora_inicio1 == hora_inicio2 or hora_fin1 == hora_fin2:
        resultado = False # sí hay superposición
    # una está contenida dentro de la otra
    elif (hora_inicio1 > hora_inicio2 and hora_fin1 < hora_fin2) or (hora_inicio2 > hora_inicio1 and hora_fin2 < hora_fin1):
        resultado = False # sí hay superposición
    # una comienza antes de que la otra termine
    elif (hora_inicio1 > hora_inicio2 and hora_inicio1 < hora_fin2) or (hora_inicio2 > hora_inicio1 and hora_inicio2 < hora_fin1):
        resultado = False # sí hay superposición
    # una termina después de que la otra haya empezado
    elif (hora_fin1 > hora_inicio2 and hora_fin1 < hora_fin2) or (hora_fin2 > hora_inicio1 and hora_fin2 < hora_fin1):
        resultado = False
    return resultado
"""        