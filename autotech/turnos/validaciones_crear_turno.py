from django.http import HttpResponse
from administracion.models import *
from .obtener_datos import *
from datetime import *
from .gestion_agenda.gestionar_agenda import *
from vehiculos.api_client.vehiculos import *

class validaciones:  
    @classmethod  
    def validaciones_generales(cls, taller_id:str, patente:str, tipo:str, dia_inicio:date, horario_inicio:time, dia_fin:date, horario_fin:time) -> HttpResponse:
        taller_valido = cls.validar_taller(taller_id= taller_id, dia_inicio=dia_inicio, horario_inicio= horario_inicio, dia_fin= dia_fin, horario_fin=horario_fin)
        if taller_valido.status_code == 400:
            return taller_valido
        dias_horarios_validos = cls.validar_dias_horarios(dia_inicio=dia_inicio, horario_inicio= horario_inicio, dia_fin= dia_fin, horario_fin=horario_fin)
        if dias_horarios_validos.status_code == 400:
            return dias_horarios_validos
        patente_valida = cls.validar_patente(patente, tipo, fecha_turno=dia_inicio, hora_turno=horario_inicio)
        if patente_valida.status_code == 400:
            return patente_valida
        return HttpResponse("Datos correctos", status=200)
    
    @classmethod  
    def validaciones_service(cls, taller_id:str, patente:str, dia_inicio:date, horario_inicio:time, dia_fin:date, horario_fin:time, km: int, frecuencia_ultimo_service:int , frecuencia_service_solicitado:int ) -> HttpResponse:
        resultado_validacion_general = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='service', 
                                                                   dia_inicio=dia_inicio, horario_inicio=horario_inicio,
                                                                   dia_fin= dia_fin, horario_fin=horario_fin)
        if resultado_validacion_general.status_code == 400:
            return resultado_validacion_general
        if not validaciones.patente_registrada(patente):
            return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)
        if km == None:
            return HttpResponse("error: el service debe tener un kilometraje asociado", status=400)
        if frecuencia_ultimo_service != 0 and frecuencia_ultimo_service >= frecuencia_service_solicitado:
            return HttpResponse("error: el service ingresado ya se había realizado antes.", status=400)
        return HttpResponse("Datos correctos", status=200)
    
    @classmethod  
    def validaciones_reparacion(cls, taller_id:str, patente:str, dia_inicio:date, horario_inicio:time, dia_fin:date, horario_fin:time, origen:str) -> HttpResponse:
        resultado_validacion_general = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='reparacion', 
                                                                   dia_inicio=dia_inicio, horario_inicio=horario_inicio,
                                                                   dia_fin= dia_fin, horario_fin=horario_fin)
        if resultado_validacion_general.status_code == 400:
            return resultado_validacion_general
        if origen == 'extraordinario':
            if not validaciones.patente_registrada(patente=patente):
                return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)  
        return HttpResponse("Datos correctos", status=200)
    
    @classmethod  
    def validaciones_extraordinario(cls, taller_id:str, patente:str, dia_inicio:date, horario_inicio:time, dia_fin:date, horario_fin:time) -> HttpResponse:
        resultado_validacion_general = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='extraordinario', 
                                                                   dia_inicio=dia_inicio, horario_inicio=horario_inicio,
                                                                   dia_fin= dia_fin, horario_fin=horario_fin)
        if resultado_validacion_general.status_code == 400:
            return resultado_validacion_general
        if not validaciones.patente_registrada(patente=patente): 
            return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)
        return HttpResponse("Datos correctos", status=200)
    
    @classmethod  
    def validar_taller(cls, taller_id:str, dia_inicio:date, horario_inicio:time, dia_fin:date, horario_fin:time) -> HttpResponse:
        if not cls.existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)
        if not cls.taller_es_valido(taller_id):
            return HttpResponse("error: el id ingresado pertenece a un taller inactivo", status=400)
        if not cls.taller_esta_disponible(taller_id, dia_inicio, horario_inicio, dia_fin, horario_fin):
            return HttpResponse("error: ese dia no esta disponible en ese horario", status=400)
        return HttpResponse("Taller correcto", status=200)
        
    @classmethod          
    def validar_dias_horarios(cls, dia_inicio:date, horario_inicio:time, dia_fin:date, horario_fin:time) -> HttpResponse:
        if not cls.horarios_exactos(horario_inicio, horario_fin):
            return HttpResponse("error: los horarios de comienzo y fin de un turno deben ser horas exactas", status=400)
        if not cls.horarios_dentro_de_rango(dia_inicio, horario_inicio):
            return HttpResponse("error: los horarios superan el limite de la jornada laboral", status=400)
        if not cls.dia_valido(dia_inicio):
            return HttpResponse("error: no se puede sacar un turno para una fecha que ya paso.", status=400)
        if not cls.dia_hora_coherentes(dia_inicio, horario_inicio, dia_fin, horario_fin):
            return HttpResponse("error: un turno no puede terminar antes de que empiece", status=400)
        return HttpResponse("Dias horarios correctos", status=200)
     
    @classmethod     
    def validar_patente(cls, patente:str, tipo:str, fecha_turno: date, hora_turno:time):
        hoy = date.today()
        condiciones_exclusion = Q(estado='terminado') | Q(estado='cancelado') | Q(estado='rechazado') | Q(estado='ausente')
        turnos_ese_tipo = Turno_taller.objects.filter(patente=patente, tipo=tipo, fecha_inicio__gte=hoy).exclude(condiciones_exclusion)
        if turnos_ese_tipo.count() != 0:
            return HttpResponse("error: la patente ingresada ya tiene un turno de ese tipo registrado en el sistema.", status=400)
        turnos_ese_dia_horario = Turno_taller.objects.filter(patente=patente, fecha_inicio= fecha_turno, hora_inicio=hora_turno)
        if turnos_ese_dia_horario.count() != 0:
            return HttpResponse("error: la patente ingresada ya tiene un turno para ese mismo dia y horario en el sistema", status=400)
        return HttpResponse("Patente correcta", status=200)
    
    # ------------------------------------------------------------------------------------------------ #
    # ----------------------------------- auxiliares y solitarias ------------------------------------ #
    # ------------------------------------------------------------------------------------------------ # 

    @classmethod
    def patente_registrada(cls, patente:str):
        existe_patente = ClientVehiculos.obtener_km_de_venta(patente=patente)
        return existe_patente

    @classmethod
    def existe_taller(cls, taller_id:int):
        try:
            taller = Taller.objects.get(id_taller= taller_id)
        except:
            return False
        else:
            return True
        
    @classmethod
    def taller_es_valido(cls, taller_id:int):
        taller = Taller.objects.get(id_taller= taller_id)
        return taller.estado == True
        
    @classmethod
    def horarios_exactos(cls, hora_inicio:time, hora_fin:time):
        return hora_inicio.minute == 0 and hora_fin.minute == 0 and hora_inicio.second == 0 and hora_fin.second == 0 # and hora_inicio <= hora_fin
            
    @classmethod
    def horarios_dentro_de_rango(cls, dia:date, horario_inicio:time):
        if dia.weekday() == 6: # domigo
            horario_inicio_valido = horario_inicio.hour >= 8 and horario_inicio.hour <= 11
        else:
            horario_inicio_valido = horario_inicio.hour >= 8 and horario_inicio.hour <= 16
        return horario_inicio_valido
        
    @classmethod
    def dia_hora_coherentes(cls, dia_inicio: date, horario_inicio: time, dia_fin: date , horario_fin: time):
        if dia_inicio < dia_fin:
            es_valido = True
        elif dia_inicio == dia_fin:
            es_valido = horario_inicio < horario_fin
        else:
            es_valido = False
        return es_valido
    
    @classmethod
    def dia_valido(cls, dia: date):
        return dia >= date.today()

    @classmethod
    def taller_esta_disponible(cls, id_taller: int, fecha_inicio:date, hora_inicio:time, fecha_fin:date, hora_fin:time):
        return taller_esta_disponible_agenda(fecha_inicio, hora_inicio, fecha_fin, hora_fin, id_taller)