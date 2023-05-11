#import requests
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from administracion.models import Turno_taller
from administracion.serializers import TurnoTallerSerializer
from datetime import date, time

@api_view(["POST"])
def asignar_tecnico(request, id_tecnico:int, id_turno: int):
    
    turno = obtener_turno(id_turno)
    
    if not turno_valido(turno):
        return HttpResponse("error: administracion no ha verificado que la documentacion esta en orden.", status=400)
    if not esta_disponible(id_tecnico):
        return HttpResponse("error: el tecnico no tiene disponible ese horario", status=400)
    
    turno.tecnico_id = id_tecnico           # agregamos el id del tecnico al turno
    turno.save()
    turno.estado = "en_proceso"
    turno.save()
    
    serializer= TurnoTallerSerializer(turno,many=False) # retornamos el turno, donde debería verse el tecnico recien asignado
    return Response(serializer.data)
    
    
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
  
"""
def coinciden_los_talleres(tecnico, turno:Turno_taller):
    print("A desarrollar")
"""
    
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

def obtener_turnos_del_tecnico(id_tecnico: int):
    return Turno_taller.objects.filter(id_tecnico = id_tecnico)

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