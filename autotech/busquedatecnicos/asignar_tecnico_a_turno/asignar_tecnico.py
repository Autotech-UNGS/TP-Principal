#import requests
from administracion.models import Turno_taller
from datetime import date, time      
    
def se_puede_asignar_tecnico(tipo_turno: str, papeles_en_regla_turno: bool):
    if tipo_turno != "Evaluacion":
        es_valido = True
    elif papeles_en_regla_turno == True:
        es_valido = True
    else:
        es_valido = False
    return es_valido
  
"""
def coinciden_los_talleres(tecnico, turno:Turno_taller):
    print("A desarrollar")
"""
    
def esta_disponible(id_tecnico: int, dia:date, hora_inicio:time, hora_fin:time):
    # Si el id del tecnico no aparece en ningun turno, da una excepcion. Para evitarlo, hacemos
    # retornamos True --> no tiene turnos, entonces esta disponible
    try:
        turnos_del_tecnico = Turno_taller.objects.filter(tecnico_id = id_tecnico)
    except:
    #if turnos_del_tecnico == None:
        return True
    else:
        turnos_del_tecnico = Turno_taller.objects.filter(tecnico_id = id_tecnico)
        esta_disponible = True
        for turno in turnos_del_tecnico:
            dia_inicio_turno_agendado = turno.fecha_inicio
            if dia_inicio_turno_agendado == dia:    # si encontramos un turno el mismo dia...
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + dia_inicio_turno_agendado)
                hora_inicio_turno_agendado = turno.hora_inicio
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + hora_inicio_turno_agendado)
                hora_fin_turno_agendado = turno.hora_fin
                print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + hora_fin_turno_agendado)
                print(hora_inicio_turno_agendado, hora_fin_turno_agendado, hora_inicio, hora_fin)
                esta_disponible = esta_disponible and no_hay_superposicion(hora_inicio_turno_agendado, hora_fin_turno_agendado, hora_inicio, hora_fin)
                #esta_disponible = not hay_superposicion(hora_inicio_turno_agendado, hora_fin_turno, hora_inicio, hora_fin)
        
        return esta_disponible
            
def no_hay_superposicion(hora_inicio1: time, hora_fin1: time, hora_inicio2: time, hora_fin2: time):
    caso1 = hora_inicio2 >= hora_fin1 # el 2 empieza cuando el 1 termina
    caso2 = hora_fin2 <= hora_inicio1 # el 2 termina cuando el 1 empieza
    caso3 = hora_inicio1 >= hora_fin2 # el 1 empieza cuando el 2 termina
    caso4 = hora_fin1 <= hora_inicio2 # el 1 termina cuando el 2 empieza
    caso5 = hora_inicio1 != hora_inicio2 # el 1 y el 2 no empiezan a la vez
    caso6 = hora_fin1 != hora_fin2 # el 1 y el 2 no terminan a la vez
    return (caso1 or caso2 or caso3 or caso4) and caso5 and caso6

"""
def obtener_tecnico(id_tecnico: int):
    url = "https://api-rest-pp1.onrender.com/api/usuarios/"
    usuarios_data = requests.get(url)

    if usuarios_data.status_code != 200:
        raise requests.HTTPError(f"Error: {usuarios_data.status_code}")

    usuarios_data = usuarios_data.json()
    tecnico = [{
        'id_empleado': tecnico['id_empleado'],
        'nombre_completo': tecnico['nombre_completo'], 
        'dni': tecnico['dni'], 
        'categoria': tecnico['categoria'], 
        'branch': tecnico['branch']
        } for tecnico in usuarios_data if tecnico['tipo'] == "Tecnico" and tecnico['id_empleado'] == id_tecnico]   
   
    return tecnico
"""