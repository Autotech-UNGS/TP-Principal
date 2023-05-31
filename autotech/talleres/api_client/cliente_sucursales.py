import requests

import json

from rest_framework.response import Response
from rest_framework import status

from administracion.models import Taller



class ClientSucursales():
    # para obtener todos las sucursales con taller y activas
    BASE_URL = "https://karu-administracion-back-desarrollo.azurewebsites.net/v1/sucursales/activas_con_taller/"

    @classmethod
    def _obtener_datos(cls, url):
        response = requests.get(url)
     
        if response.status_code != 200:
            
           return Response({'error': response.status_code})

        data = response.json()
        return data

    @classmethod
    def obtener_sucursales(cls):
        response = cls._obtener_datos(cls.BASE_URL)
        return response
    
    @classmethod
    def obtener_sucursal(cls, id_sucursal):
        sucursales = cls._obtener_datos(cls.BASE_URL)

        for sucursal in sucursales:
            if sucursal["id"] == id_sucursal:
                return sucursal

        raise Exception(f'No se encontró la sucursal {id_sucursal}')
    
    @classmethod
    def obtener_valor_clave(cls, id_sucursal ,clave):
        sucursales = cls._obtener_datos(cls.BASE_URL)

        for sucursal in sucursales:
            if sucursal["id"] == id_sucursal:
                try:
                    return sucursal[clave]
                except:
                    raise Exception(f'No se encontró la clave: {clave}')
                    

        raise Exception(f'No se encontró la sucursal: {id_sucursal}')
    
    @classmethod
    def obtener_sucursales_sin_talller(cls):

        sucursales = cls._obtener_datos(cls.BASE_URL)
        sucursales_sin_taller = []

        talleres_ids = set(Taller.objects.values_list('id_sucursal', flat=True))

        for sucursal in sucursales:
            if sucursal["id"] not in talleres_ids:
                    sucursales_sin_taller.append(sucursal)

        return sucursales_sin_taller
    

    @classmethod
    def tiene_taller(cls, id_sucursal):

        sucursales = cls._obtener_datos(cls.BASE_URL)

        

        return tiene
  