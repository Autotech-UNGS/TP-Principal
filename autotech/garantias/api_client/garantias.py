import requests
from datetime import date, time, datetime


class ClientGarantias():
    #BASE_URL_FACTURA = inserte url aqui
    #BASE_URL_ACTUALIZAR_ESTADO = inserte url aqui
    
    @classmethod
    def obtener_estado(cls, patente:str):
        factura = cls.obtener_datos_factura(patente)
        if factura:
            estado_anulado = factura.get("estado")
            return 'anulada' if estado_anulado else 'no_anulada'
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
    def obtener_datos_factura(cls, patente: str):
        url = f'{cls.BASE_URL_FACTURA}{patente}'
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError({'message error': response.status_code})

        datos_factura = response.json()
        return datos_factura
        
    @classmethod    
    def informar_perdida_garantia(cls, patente: str):
        url = f'{cls.BASE_URL_ACTUALIZAR_ESTADO}{patente}'
        data = {'estado': True}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.HTTPError({'message error': response.status_code})