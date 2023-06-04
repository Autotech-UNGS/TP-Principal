from administracion.models import Taller, Service, Turno_taller, Registro_evaluacion_para_admin, Checklist_evaluacion, Registro_extraordinario, Registro_service
from datetime import date, time, timedelta
from math import ceil
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from vehiculos.api_client.vehiculos import *
from clientes.api_client.clientes import *

# ------------------------------------------------------------------------------------------------ #
# ---------------------------------------- envío de emails --------------------------------------- #
# ------------------------------------------------------------------------------------------------ # 

def obtener_email_usuario(patente:str):
    #return "luciacsoria5@gmail.com"
    try:
        dni = ClientVehiculos.obtener_dni_cliente(patente)
        email = ClientClientes.obtener_email(dni)
        return email
    except:
        return None
  
  
def obtener_direccion_taller(taller_id) -> str:
    taller = Taller.objects.get(id_taller= taller_id)
    return f'{taller.direccion}, {taller.localidad}, {taller.provincia}.'

# ------------------------------------------------------------------------------------------------ #
# -------------------------------------- datos del vehículo -------------------------------------- #
# ------------------------------------------------------------------------------------------------ # 

def obtener_marca(patente:str) -> str:
    marca = ClientVehiculos.obtener_marca(patente=patente)
    return marca

def obtener_modelo(patente:str) -> str:
    modelo = ClientVehiculos.obtener_modelo(patente=patente)
    return modelo

def obtener_km_de_venta(patente) -> int:
    km = ClientVehiculos.obtener_km_de_venta(patente=patente)
    km = redondear_a_multiplo_de_cincomil(km)
    return km

def redondear_a_multiplo_de_cincomil(km):
    resultado = round(int(km) / 5000) * 5000
    return resultado if resultado != 0 else 5000

# ------------------------------------------------------------------------------------------------ #
# ------------------------------------ frecuencia de services ------------------------------------ #
# ------------------------------------------------------------------------------------------------ # 

def obtener_frecuencia_service_solicitado(patente:str, kilometraje_actual: int):
    km_de_venta = obtener_km_de_venta(patente)
    # kilometraje actual - kilometraje inicial = diferencia de km (o sea, km del nuevo service)
    frecuencia_service = kilometraje_actual - km_de_venta
    return frecuencia_service

def obtener_frecuencia_ultimo_service(patente:str):
    try:
        # ultimo turno de service de x patente --> Registro_service de ese turno --> Service
        ultimo_turno_service = Turno_taller.objects.filter(patente=patente, tipo='service', estado="terminado").latest('fecha_inicio')
        registro_de_ultimo_service = Registro_service.objects.get(id_turno=ultimo_turno_service.id_turno)
        ultimo_service = Service.objects.get(id_service=registro_de_ultimo_service.id_service.id_service)
        return ultimo_service.frecuencia_km
    except:
        return 0
    
# ------------------------------------------------------------------------------------------------ #
# ------------------------------------ fecha/hora final, turno ----------------------------------- #
# ------------------------------------------------------------------------------------------------ # 

#[fecha_fin, hora_fin]
def obtener_fecha_hora_fin(dia_inicio:date, horario_inicio:time, duracion:int) -> list: 
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

def obtener_turno(id_turno):
    try:
        turno = Turno_taller.objects.get(id_turno= id_turno)
        return turno
    except:
        return None

# ------------------------------------------------------------------------------------------------ #
# -------------------------------------- duracion de turnos -------------------------------------- #
# ------------------------------------------------------------------------------------------------ # 

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
            if fecha == fecha_fin and hora == hora_fin:
                seguir = False
            if (hora.hour == 17 and fecha.weekday() != 6) or (hora.hour == 12 and fecha.weekday() == 6):
                hora = time(8,0,0)
                fecha = fecha + timedelta(days=1)
    return duracion

# para crear un turno
# retorna 0 si el service no existe
def obtener_duracion_service_vehiculo(patente:str, km:int):
    try:
        marca = obtener_marca(patente)
        modelo = obtener_modelo(patente)
        service = Service.objects.get((Q(marca=marca) & Q(modelo=modelo) & Q(frecuencia_km=km)) | (Q(marca="generico") & Q(modelo="generico") & Q(frecuencia_km=km)), activo=True)
    except ObjectDoesNotExist:
        return 0
    resultado = ceil(service.duracion_total / 60)
    return resultado
        
# para obtener la duracion de un service en específico
# retorna 0 si el service no existe        
def obtener_duracion_service(marca:str, modelo:str, km:int):
    try:
        service = Service.objects.get(marca=marca, modelo=modelo, frecuencia_km=km)
        return ceil(service.duracion_total / 60)
    except:
        return 0    

# viene de venta        
# retorna 0 si no existe un turno para evaluacion para esa patente
def obtener_duracion_reparacion(patente:str): 
    try:
        turno = Turno_taller.objects.filter(patente=patente, tipo= 'evaluacion', estado="terminado").latest('fecha_inicio')
        registro_admin = Registro_evaluacion_para_admin.objects.get(id_turno=turno.id_turno)
        return ceil(registro_admin.duracion_total_reparaciones / 60)
    except:
        return 0
    
# viene de extraordinario    
# retorna 0 si no existe un turno para evaluacion para esa patente
def obtener_duracion_extraordinario(patente:str):
    try:
        turno = Turno_taller.objects.filter(patente=patente, tipo= 'extraordinario', estado="terminado").latest('fecha_inicio')
        registro_extraordinario = Registro_extraordinario.objects.get(id_turno=turno.id_turno)
        lista_task = registro_extraordinario.id_tasks
        duracion = 0
        for id in lista_task:
            item = Checklist_evaluacion.objects.get(id_task = id)
            duracion += item.duracion_reemplazo
        return ceil(duracion / 60) 
    except Exception:
        return 0
