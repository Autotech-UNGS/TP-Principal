from django.http import HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from ..gestion_garantia import GestionGarantias
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from datetime import datetime
from turnos.obtener_datos import *

class VerificarEstadoGarantia(ViewSet):    
    
    @action(detail=True, methods=['get'])
    def garantia_vigente(self, request, patente:str, fecha_turno:str, service_solicitado:int):
        service_solicitado = redondear_a_multiplo_de_cincomil(service_solicitado)
        patente = patente.upper()
        if not patente_registrada(patente=patente):
            return HttpResponse(f"error: la patente no está registrada como perteneciente a un cliente: {patente}", status=400)
        
        fecha_turno =datetime.strptime(fecha_turno, '%Y-%m-%d').date()
        ultimo_service = obtener_frecuencia_ultimo_service(patente)
        km_solicitado = obtener_frecuencia_service_solicitado(patente=patente, kilometraje_actual=service_solicitado)
        
        if service_solicitado <= obtener_km_de_venta(patente=patente):
                return HttpResponse(f"error: el service ingresado no es valido: se solicita un service de {service_solicitado}km para un vehiculo vendido con {obtener_km_de_venta(patente)}km", status=400)            
        if ultimo_service != 0 and ultimo_service >= km_solicitado:
                return HttpResponse(f"error: el service ingresado ya se había realizado antes: service de {ultimo_service}, {patente}", status=400)
        
        #mantiene_garantia = GestionGarantias.garantia_seguiria_vigente(patente, fecha_turno, ultimo_service, service_actual)
        try:
            motivo = motivo_perdida_garantia(patente=patente, fecha_turno=fecha_turno, ultimo_service=ultimo_service, service_solicitado=km_solicitado)
        except Exception:
            return HttpResponse(f"error: El vehiculo con la patente ingresada no fue vendido o no se le ha creado una factura: {patente}", status=400)
        if motivo != "":
            costo_total = obtener_costo_base_service_vehiculo(patente=patente, km_solicitado=km_solicitado) + obtener_costo_total_service_vehiculo(patente=patente, km_solicitado=km_solicitado)
            if costo_total == 0:
                return HttpResponse(f"error: no existe un service con los datos especificados: {km_solicitado}", status=400)
            mensaje = f"La patente {patente} no sigue en garantía, debido a que {motivo} El service tendrá un costo total de hasta: ${costo_total}"
        else:
            costo_base = obtener_costo_base_service_vehiculo(patente=patente, km_solicitado=km_solicitado)
            if costo_base == 0:
                return HttpResponse(f"error: no existe un service con los datos especificados: {km_solicitado}", status=400)
            mensaje = f"La patente {patente} sigue en garantia. El service tendrá un costo base de: ${costo_base}"
        mensaje = mensaje.replace("\n", " ")
        return HttpResponse(mensaje, status=200)
        
    @action(detail=True, methods=['get'])
    def estado_garantia(self, request, patente:str):
        patente = patente.upper()
        if not patente_registrada(patente=patente):
            return HttpResponse(f"error: la patente no está registrada como perteneciente a un cliente: {patente}", status=400)
        try:
            estado = GestionGarantias.estado_garantia(patente=patente)
            return HttpResponse(estado, status=200)
        except ValueError as e:
            return HttpResponse(e, status=400)
        
    # pierde garantía a partir de los 15k o si ya pasó un año desde que el cliente compro el auto
    # perde la garantía si se salteó services
def motivo_perdida_garantia(patente:str, fecha_turno:date, ultimo_service:int, service_solicitado:int):
    try:
        if GestionGarantias.estado_garantia(patente) == 'anulada':
            return "la misma llegó a su fin o ha sido anulada anteriormente."
        
        duracion = GestionGarantias.obtener_duracion_garantia(patente=patente)
        if not GestionGarantias.tiempo_valido(patente, fecha_turno):
            return f"ha expirado el tiempo de cobertura de la misma (fecha de vencimiento: {GestionGarantias.obtener_tiempo_maximo(patente=patente)})."
        
        elif not GestionGarantias.km_en_tiempo(patente, service_solicitado):
            return f"ha alcanzado el límite de cobertura de la misma ({duracion * 15000} kilometros)."
        
        elif not GestionGarantias.no_salteo_service(ultimo_service, service_solicitado):
            return f"se ha salteado el service de {ultimo_service + 5000} kilometros."
        return ""
    except Exception as e:
            raise HttpResponse(e, status=400)
    
def patente_registrada(patente:str):
    existe_patente = ClientVehiculos.patente_registrada_vendido(patente=patente)
    return existe_patente