import requests
import json

class ClientClientes:
    BASE_URL_DNI = 'http://34.139.89.18:8181/api-gc/clientes/cliente?dni='
    
    @classmethod
    def obtener_email(cls, dni):
        cliente = cls.obtener_datos_cliente(dni)
        email = cliente.get("email")
        return email
        
    @classmethod    
    def obtener_datos_cliente(cls, dni: str):
        url = f'{cls.BASE_URL_DNI}{dni}'
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.HTTPError({'message error': response.status_code})

        datos_cliente = response.json()
        
        return datos_cliente