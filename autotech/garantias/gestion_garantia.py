from datetime import date, timedelta
from .api_client.garantias import *
 
class GestionGarantias:
    
    @classmethod
    def garantia_seguiria_vigente(cls, patente:str, fecha_turno:date, ultimo_service:int, service_solicitado:int):
        if cls.estado_garantia(patente) != 'no_anulada':
            return False
        garantia_vigente = cls.tiempo_valido(patente, fecha_turno) and cls.km_en_tiempo(patente, service_solicitado) and cls.no_salteo_service(ultimo_service, service_actual)
        return garantia_vigente
    
    @classmethod
    def informar_perdida_garantia(cls, patente:str):
        #TODO
        return True
    
    @classmethod
    def estado_garantia(cls, patente) -> str:
        """
        try:
            estado = ClientGarantias.obtener_estado(patente=patente)
            return estado
        except ValueError as e:
            return e
        """
        return 'no_anulada'
    
    @classmethod
    def km_en_tiempo(cls, patente:str, kilometraje: int) -> bool: 
        duracion = cls.obtener_duracion_garantia(patente)
        km_limite = 15000 * duracion
        return kilometraje <= km_limite
    
    @classmethod
    def no_salteo_service(cls, ultimo_service, service_actual) -> bool:
        return ultimo_service + 5000 == service_actual
    
    @classmethod
    def tiempo_valido(cls, patente:str, fecha_turno:date) -> bool:
        tiempo_maximo = cls.obtener_tiempo_maximo(patente)
        return fecha_turno <= tiempo_maximo
    
    @classmethod
    def obtener_tiempo_maximo(cls, patente:str) -> date:
        duracion_garantia = cls.obtener_duracion_garantia(patente)
        dia_de_venta = cls.obtener_dia_de_venta(patente)
        if not (dia_de_venta.month == 2 and dia_de_venta.day == 29):
            vencimiento = date(dia_de_venta.year + duracion_garantia, dia_de_venta.month, dia_de_venta.day)
        else:
            vencimiento = date(dia_de_venta.year + duracion_garantia, 3, 1)
        return vencimiento
        
    @classmethod
    def obtener_duracion_garantia(cls, patente:str) -> int:
        """
        try:
            tipo = ClientGarantias.obtener_tipo(patente=patente)
            return 1 if tipo == 'normal' else 2
        except ValueError as e:
            return e
        """
        return 1 # 1 año
    
    @classmethod
    def obtener_dia_de_venta(cls, patente:str) -> date:
        """
        try:
            dia = ClientGarantias.obtener_dia_de_venta(patente=patente)
            return dia
        except ValueError as e:
            return e
        """
        maniana = date.today() + timedelta(days=1)
        return date(maniana.year -1, maniana.month, maniana.day)
        