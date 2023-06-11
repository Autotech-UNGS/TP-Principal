from datetime import date, timedelta
from .api_client.garantias import *
 
class GestionGarantias:
    
    @classmethod
    def garantia_seguiria_vigente(cls, patente:str, fecha_turno:date, ultimo_service:int, service_solicitado:int):
        try:
            if cls.estado_garantia(patente) == 'anulada':
                return False
            garantia_vigente = cls.tiempo_valido(patente, fecha_turno) and cls.km_en_tiempo(patente, service_solicitado) and cls.no_salteo_service(ultimo_service, service_solicitado)
            return garantia_vigente
        except Exception as e:
            raise e
        
    @classmethod
    def informar_perdida_garantia(cls, patente:str):
        try:
            ClientGarantias.informar_perdida_garantia(patente=patente)
            print("garantia modificada")
            return True
        except ValueError as e:
            raise e
    
    @classmethod
    def estado_garantia(cls, patente) -> str:
        try:
            estado = ClientGarantias.obtener_estado(patente=patente)
            return estado
        except ValueError as e:
            raise e
    
    @classmethod
    def km_en_tiempo(cls, patente:str, kilometraje: int) -> bool: 
        try:
            duracion = cls.obtener_duracion_garantia(patente)
            km_limite = 15000 * duracion
            return kilometraje <= km_limite
        except Exception as e:
            raise e
    
    @classmethod
    def no_salteo_service(cls, ultimo_service, service_actual) -> bool:
        return ultimo_service + 5000 == service_actual
    
    @classmethod
    def tiempo_valido(cls, patente:str, fecha_turno:date) -> bool:
        try:
            tiempo_maximo = cls.obtener_tiempo_maximo(patente)
            return fecha_turno <= tiempo_maximo
        except Exception as e:
            raise e
    
    @classmethod
    def obtener_tiempo_maximo(cls, patente:str) -> date:
        try:
            duracion_garantia = cls.obtener_duracion_garantia(patente)
            dia_de_venta = cls.obtener_dia_de_venta(patente)
            if not (dia_de_venta.month == 2 and dia_de_venta.day == 29):
                vencimiento = date(dia_de_venta.year + duracion_garantia, dia_de_venta.month, dia_de_venta.day)
            else:
                vencimiento = date(dia_de_venta.year + duracion_garantia, 3, 1)
            return vencimiento
        except Exception as e:
            raise e
            
    @classmethod
    def obtener_duracion_garantia(cls, patente:str) -> int:
        try:
            tipo = ClientGarantias.obtener_tipo(patente=patente)
            return 1 if tipo == 'normal' else 2
        except ValueError as e:
            raise e
    
    @classmethod
    def obtener_dia_de_venta(cls, patente:str) -> date:
        try:
            dia = ClientGarantias.obtener_dia_de_venta(patente=patente)
            return dia
        except ValueError as e:
            raise e
        