from datetime import date, time, datetime
from administracion.models import Turno_taller

def asignar_tecnico(id_tecnico:int, id_turno: int):
    tecnico = obtener_tecnico(id_tecnico)
    turno = obtener_turno(id_turno)
    
    if not turno_valido(turno):
        raise ValueError("El turno no paso la prueba de papeles aun")
    if not coinciden_los_talleres(tecnico, turno):
        raise ValueError("El tecnico no trabaja en el taller de ese turno")
    if not esta_disponible(id_tecnico):
        raise ValueError("El tecnico no tiene disponible ese horario")
    
    turno.tecnico_id = id_tecnico   # agregamos el id del tecnico al turno
    asignar_turno(tecnico, turno.id_turno) # esto es un POST a la api de tecnicos, creo
    turno.estado = "en_proceso"
    
def obtener_turno(id_turno) -> Turno_taller:
    return Turno_taller.objects.get(id_turno=id_turno) # debería ser uno sólo      
    
def turno_valido(turno: Turno_taller):
    if turno.tipo != "EVALUACION":
        es_valido = True
    elif turno.papeles_en_regla == True:
        es_valido = True
    else:
        es_valido = False
    return es_valido
  
 #TODO 
def coinciden_los_talleres(tecnico, turno:Turno_taller):
    print("TODO")
    
def esta_disponible(id_tecnico: int, dia:date, hora_inicio:time, hora_fin:time):
    turnos_del_tecnico = obtener_turnos_del_tecnico(id_tecnico)
    esta_disponible = True
    
    for turno in turnos_del_tecnico:
        dia_inicio_turno = turno.fecha_inicio
        if dia_inicio_turno == dia:
            hora_inicio_turno = turno.hora_inicio
            hora_fin_turno = turno.hora_fin
            esta_disponible = esta_disponible and not hay_superposicion(hora_inicio_turno, hora_fin_turno, hora_inicio, hora_fin)
    
    return esta_disponible
            
def hay_superposicion(hora_inicio1: time, hora_fin1: time, hora_inicio2: time, hora_fin2: time):
    caso1 = hora_inicio2 >= hora_fin1 # el 2 empieza cuando el 1 termina
    caso2 = hora_fin2 <= hora_inicio1 # el 2 termina cuando el 1 empieza
    caso3 = hora_inicio1 >= hora_fin2 # el 1 empieza cuando el 2 termina
    caso4 = hora_fin1 <= hora_inicio2 # el 1 termina cuando el 2 empieza
    return caso1 or caso2 or caso3 or caso4
    
#TODO    
def obtener_tecnico(id_tecnico: int):
    print("TODO")
    
#TODO    
def asignar_turno(tecnico, id_turno: int):
    print("TODO")

def obtener_turnos_del_tecnico(id_tecnico: int):
    return Turno_taller.objects.filter(id_tecnico = id_tecnico)