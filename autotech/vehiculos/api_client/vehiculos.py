import requests
import json

class ClientVehiculos():
    BASE_URL_PATENTE = 'https://gadmin-backend-production.up.railway.app/api/v1/vehicle/getByPlate/'
    
    @classmethod
    def obtener_dni_cliente(cls, patente:str):
        #return "1234568"    
        datos_vehiculo = cls.obtener_datos_vehiculo(patente)
        if datos_vehiculo:
            dni = datos_vehiculo.get("dni")
            return dni
        return None
        
    @classmethod
    def patente_registrada(cls, patente:str):
        datos_vehiculo = cls.obtener_datos_vehiculo(patente)
        if datos_vehiculo:
             if datos_vehiculo.get("status") == 'VENDIDO':
                return True
        return False
    
    @classmethod
    def obtener_marca_modelo(cls, patente:str):
        datos_vehiculo = cls.obtener_datos_vehiculo(patente)
        if datos_vehiculo and datos_vehiculo.get("status") == 'VENDIDO':
            marca = datos_vehiculo.get("brand")
            modelo = datos_vehiculo.get("model")
            return marca, modelo
        raise ValueError(f"Patente no existente: {patente}")
    
    @classmethod
    def obtener_km_de_venta(cls, patente:str):
        datos_vehiculo = cls.obtener_datos_vehiculo(patente)
        if datos_vehiculo and datos_vehiculo.get("status") == 'VENDIDO':
            km = datos_vehiculo.get("kilometers")
            return km
        raise ValueError(f"La patente no pertenece a un vehiculo vendido a un cliente: {patente}")
        
    @classmethod    
    def obtener_datos_vehiculo(cls, patente: str):
        url = f'{cls.BASE_URL_PATENTE}{patente}'
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError({'message error': response.status_code})

        data = response.json()
        datos_vehiculo = data.get("result")
        if datos_vehiculo and "error" in datos_vehiculo:
            error = datos_vehiculo["error"]
            errorCode = error.get("code")
            name = error.get("name")
            message = error.get("message")
            value = error.get("value")

            raise ValueError(f"Error al obtener los datos del vehiculo. Código: {errorCode}, Nombre: {name}, Mensaje: {message}, Valor: {value}")
        else:
            return datos_vehiculo
        