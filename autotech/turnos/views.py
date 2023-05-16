import requests
from django.http import JsonResponse, HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .validaciones_views import * 
from datetime import *

@api_view(['GET'])
def turnosOverview(request):
    turnos_urls={
        'List':'turnos-list/',
        'Detalle':'turnos-detalle/<str:id_turno>/',
        'DiasHorariosDisponibles':'dias-horarios-disponibles/<str:taller_id>',
        'Create':'turnos-create/',
        'Update':'turnos-update/<int:id_turno>/',
        'Asignar-tecnico':'asignar-tecnico/<int:id_tecnico>/<int:_id_turno>/'
    }
    return Response(turnos_urls)

@api_view(['GET'])
def turnosList(request):
    turnos= Turno_taller.objects.all()
    serializer= TurnoTallerSerializer(turnos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def turnoDetalle(request, id_turno):
    try:
        turno=Turno_taller.objects.get(id_turno=id_turno)
    except:
        return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
    else:
        serializer= TurnoTallerSerializer(turno,many=False)
        return Response(serializer.data)

@api_view(['GET'])
def diasHorariosDisponibles(request, taller_id: int):
    try:
        taller = Taller.objects.get(id_taller= taller_id)
    except:
        return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)
    else:
        dias_horarios_data = dias_horarios_disponibles_treinta_dias(taller_id)
        resultado = [{'dia': dia, 'horarios_disponibles':dias_horarios_data.get(dia)} for dia in dias_horarios_data]
        return JsonResponse({'dias_y_horarios':resultado})

@api_view(['POST'])
def crearTurno(request):
    dia = request.data.get("fecha_inicio")
    dia_fin = request.data.get("fecha_fin")
    horario_inicio = request.data.get("hora_inicio")
    horario_fin = request.data.get("hora_fin")
    taller_id = request.data.get("taller_id")
    tipo = request.data.get("tipo")
    km = request.data.get("frecuencia_km")

    horario_inicio_time = datetime.strptime(horario_inicio, '%H:%M:%S').time()
    horario_fin_time = datetime.strptime(horario_fin, '%H:%M:%S').time()
    dia_inicio_date = datetime.strptime(dia, '%Y-%m-%d').date()
    dia_fin_date = datetime.strptime(dia_fin, '%Y-%m-%d').date()

    if tipo == "Service" and km == "":
        return HttpResponse("error: el service debe tener un kilometraje asociado", status=400)
    if not horarios_exactos(horario_inicio_time, horario_fin_time):
        return HttpResponse("error: los horarios de comienzo y fin de un turno deben ser horas exactas", status=400)
    if not horarios_dentro_de_rango(dia_inicio_date, horario_inicio_time, horario_fin_time):
        return HttpResponse("error: los horarios superan el limite de la jornada laboral", status=400)
    if not dia_valido(dia_inicio_date):
        return HttpResponse("error: no se puede sacar un turno para una fecha que ya paso.", status=400)
    if not dia_hora_coherentes(dia_inicio_date, horario_inicio_time, dia_fin_date , horario_fin_time):
        return HttpResponse("error: un turno no puede terminar antes de que empiece", status=400)
    if not esta_disponible(dia_inicio_date, horario_inicio_time, horario_fin_time, taller_id):
        return HttpResponse("error: ese dia no esta disponible en ese horario", status=400)

    serializer=TurnoTallerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

@api_view(['POST'])
def turnoUpdate(request, id_turno):
    try:
        turno=Turno_taller.objects.get(id_turno=id_turno)
    except:
        return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
    else:
        serializer=TurnoTallerSerializer(instance=turno,data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    
@api_view(['GET'])
def tecnicos_disponibles(request, id_turno: int):
    try:
        turno=Turno_taller.objects.get(id_turno=id_turno)
    except:
        return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
    else:
        tecnicos_disponibles = obtener_tecnicos_disponibles(turno.id_turno, turno.taller_id.id_taller)
        resultado = [{'id_tecnico': tecnico} for tecnico in tecnicos_disponibles]
        return JsonResponse({'tecnicos_disponibles':resultado})
    

@api_view(["POST"])
def asignar_tecnico(request, id_tecnico:int, id_turno: int):
    try:
        turno=Turno_taller.objects.get(id_turno=id_turno)
    except:
        return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
    else:
        tipo_turno = turno.tipo
        papeles_en_regla_turno = turno.papeles_en_regla
        dia_inicio_turno = turno.fecha_inicio
        hora_inicio_turno = turno.hora_inicio
        dia_fin_turno = turno.fecha_fin
        hora_fin_turno = turno.hora_fin
        tecnico_asignado = turno.tecnico_id
        
        if tecnico_asignado != None:
            return HttpResponse("error: el turno ya fue asignado.", status=400)
        if not coinciden_los_talleres(id_tecnico, turno.taller_id.id_taller):
            return HttpResponse("error: el turno no esta asignado al taller donde el tecnico trabaja.", status=400)
        if not se_puede_asignar_tecnico(tipo_turno, papeles_en_regla_turno):
            return HttpResponse("error: administracion no ha aprobado la documentacion.", status=400)
        if not esta_disponible(id_tecnico,dia_inicio_turno, hora_inicio_turno, dia_fin_turno, hora_fin_turno):
            return HttpResponse("error: el tecnico no tiene disponible ese horario", status=400)
        
        turno.tecnico_id = id_tecnico  # agregamos el id del tecnico al turno
        turno.save()
        turno.estado = "En proceso" # cambiamos el estado del turno
        turno.save()
        
        serializer= TurnoTallerSerializer(turno,many=False) # retornamos el turno, donde debería verse el tecnico recien asignado
        return Response(serializer.data)