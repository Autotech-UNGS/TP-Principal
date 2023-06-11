import requests
from datetime import date, time, datetime


class ClientGarantias():
    BASE_URL_FACTURA = "https://api-gc.epicgamer.org/api-gc/facturas/garantia?patente="
    
    @classmethod
    def obtener_estado(cls, patente:str):
        factura = cls.obtener_datos_factura(patente)
        if factura:
            esta_anulada = factura.get("garantiaAnulada")
            return 'anulada' if esta_anulada else 'no_anulada'
        raise ValueError(f"No existe una factura asociada a la patente: {patente}")
        
    @classmethod
    def obtener_dia_de_venta(cls, patente:str):
        factura = cls.obtener_datos_factura(patente)
        if factura:
            fecha = factura.get("fecha")
            return datetime.strptime(fecha, '%d-%m-%Y').date()
        raise ValueError(f"No existe una factura asociada a la patente: {patente}") 
    
    @classmethod
    def obtener_tipo(cls, patente:str):
        factura = cls.obtener_datos_factura(patente)
        if factura:
            es_extendida = factura.get("garantiaExtendida")  # si es extendida, el tipo es True, si es normal, es False
            return 'extendida' if es_extendida else 'normal'
        raise ValueError(f"No existe una factura asociada a la patente: {patente}")       
      
    @classmethod    
    def obtener_datos_factura(cls, patente: str):
        url = f'{cls.BASE_URL_FACTURA}{patente}'
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError({'message error': response.status_code})

        datos_factura = response.json()
        return datos_factura
        
    @classmethod    
    def informar_perdida_garantia(cls, patente: str):
        url = f"https://api-gc.epicgamer.org/api-gc/facturas/anular-garantia?patente={patente}&garantiaAnulada=true"
        response = requests.put(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.HTTPError({'message error': response.status_code})