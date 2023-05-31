from datetime import date, timedelta
 
class GestionGarantias:
    
    @classmethod
    def informar_perdida_garantia(cls, patente:str):
        #TODO
        return True
        
    # pierde garantía a partir de los 15k o si ya pasó un año desde que el cliente compro el auto
    # perde la garantía si se salteó services
    @classmethod
    def garantia_vigente(cls, patente:str, fecha_turno:date, ultimo_service:int, service_actual:int):
        if cls.estado_garantia(patente) != 'vigente':
            return False
        garantia_vigente = cls.tiempo_valido(patente, fecha_turno) and cls.km_en_tiempo(patente, service_actual) and cls.no_salteo_service(ultimo_service, service_actual)
        return garantia_vigente
    
    @classmethod
    def estado_garantia(cls, patente) -> str:
        #TODO
        return 'vigente'
    
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
        vencimiento = date(dia_de_venta.year + duracion_garantia, dia_de_venta.month, dia_de_venta.day)
        return vencimiento
        
    @classmethod
    def obtener_duracion_garantia(cls, patente:str) -> int:
        #TODO
        return 1 # 1 año
    
    @classmethod
    def obtener_dia_de_venta(cls, patente:str) -> date:
        #TODO
        hoy = date.today()
        return date(hoy.year -1, hoy.month, hoy.day)
        