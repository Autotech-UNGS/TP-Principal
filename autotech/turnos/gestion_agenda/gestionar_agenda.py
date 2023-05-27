from .agenda import Agenda
from datetime import date, timedelta, time
from administracion.models import Taller
from administracion.models import Turno_taller
from django.db.models import Q

# -------------- agenda de taller -------------- #

def taller_esta_disponible_agenda(fecha_inicio:date, hora_inicio:time, fecha_fin:date, hora_fin:time, id_taller:int) -> bool:
    try:
        taller = Taller.objects.get(id_taller = id_taller)
    except:
        return True
    else:
        agenda = crear_agenda_taller(id_taller)
        cargar_turnos_taller(fecha_inicio, agenda, id_taller)
        duracion = calcular_duracion(fecha_inicio, hora_inicio, fecha_fin, hora_fin)
        
        return agenda.esta_disponible(fecha_inicio, hora_inicio.hour, duracion)

def dias_disponibles_desde_hoy_a_treinta_dias(id_taller: int, cant_horas:int):
    agenda = crear_agenda_taller(id_taller)
    cargar_turnos_desde_hoy_a_treinta_dias(agenda, id_taller)
    dias_horarios_disponibles = {}
    dias_horarios_disponibles = agenda.dias_horarios_disponibles_de_treinta_dias(date.today(), cant_horas)
    return dias_horarios_disponibles

def dias_disponibles_desde_hoy_a_cuarentaycinco_dias(id_taller: int, cant_horas:int):
    agenda = crear_agenda_taller(id_taller)
    cargar_turnos_desde_hoy_a_cuarentaycinco_dias(agenda, id_taller)
    dias_horarios_disponibles = {}
    dias_horarios_disponibles = agenda.dias_horarios_disponibles_de_cuarentaycinco_dias(date.today(), cant_horas)
    return dias_horarios_disponibles

def crear_agenda_taller(_id_taller: int):
    taller = Taller.objects.get(id_taller = _id_taller)
    capacidad = taller.capacidad
    return Agenda(capacidad)

def cargar_turnos_desde_hoy_a_treinta_dias(agenda:Agenda, id_taller:int):
    dia = date.today()
    for i in range(32):
        cargar_turnos_taller(dia, agenda, id_taller)
        dia = dia + timedelta(days=1) 
        
def cargar_turnos_desde_hoy_a_cuarentaycinco_dias(agenda:Agenda, id_taller:int):
    dia = date.today()
    for i in range(47):
        cargar_turnos_taller(dia, agenda, id_taller)
        dia = dia + timedelta(days=1)         

def cargar_turnos_taller(dia:date, agenda:Agenda, id_taller:int):
    condiciones_exclusion = Q(estado='terminado') | Q(estado='cancelado') | Q(estado='rechazado') | Q(estado='ausente')
    turnos = Turno_taller.objects.filter(fecha_inicio=dia, taller_id=id_taller).exclude(condiciones_exclusion)
    
    for turno in turnos:
        duracion = calcular_duracion(turno.fecha_inicio, turno.hora_inicio, turno.fecha_fin, turno.hora_fin)
        agenda.cargar_turno(turno.fecha_inicio, turno.hora_inicio.hour, duracion)
        
# -------------- agenda de tecnico -------------- #        

def tecnico_esta_disponible_agenda(fecha_inicio:date, hora_inicio:time, fecha_fin:date, hora_fin:time, id_tecnico:int) -> bool:
    try:
        condiciones_exclusion = Q(estado='terminado') | Q(estado='cancelado') | Q(estado='rechazado') | Q(estado='ausente')
        turnos_del_tecnico = Turno_taller.objects.filter(tecnico_id= id_tecnico).exclude(condiciones_exclusion)
    except:
        return True
    else:
        agenda = crear_agenda_tecnico()
        cargar_turnos_tecnico(id_tecnico, agenda, turnos_del_tecnico)
        duracion = calcular_duracion(fecha_inicio, hora_inicio, fecha_fin, hora_fin)
        
        return agenda.esta_disponible(fecha_inicio, hora_inicio.hour, duracion)
            
def crear_agenda_tecnico():
    capacidad = 1
    return Agenda(capacidad)       

def cargar_turnos_tecnico(id_tecnico: int, agenda: Agenda, turnos_del_tecnico: list):
    for turno in turnos_del_tecnico:
        duracion = calcular_duracion(turno.fecha_inicio, turno.hora_inicio, turno.fecha_fin, turno.hora_fin)
        agenda.cargar_turno(turno.fecha_inicio, turno.hora_inicio.hour, duracion)

# -------------- duracion -------------- #

def calcular_duracion(fecha_inicio: date, hora_inicio: time, fecha_fin: date, hora_fin: time):
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
                
                
            