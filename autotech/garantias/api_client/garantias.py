import requests
from datetime import date, time, datetime


class ClientGarantias():
    #BASE_URL_FACTURA = inserte url aqui
    
    @classmethod
    def obtener_estado(cls, patente:str):
        factura = cls.obtener_datos_factura(patente)
        if factura:
            estado = factura.get("estado")
            return 'anulada' if estado else 'no_anulada'
        raise ValueError(f"No existe una factura asociada a la patente: {patente}")
        
    @classmethod
    def obtener_dia_de_venta(cls, patente:str):
        factura = cls.obtener_datos_factura(patente)
        if factura:
            fecha = factura.get("fecha")
            return datetime.strptime(fecha, '%Y-%m-%d').date()
        raise ValueError(f"No existe una factura asociada a la patente: {patente}") 
    
    @classmethod
    def obtener_tipo(cls, patente:str):
        factura = cls.obtener_datos_factura(patente)
        if factura:
            tipo = factura.get("tipo")
            return 'extendida' if tipo else 'normal'
        raise ValueError(f"No existe una factura asociada a la patente: {patente}")       
      
    @classmethod    
    def obtener_datos_cliente(cls, dni: str):
        url = f'{cls.BASE_URL_DNI}{dni}'
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError({'message error': response.status_code})

        datos_cliente = response.json()
        return datos_cliente
        