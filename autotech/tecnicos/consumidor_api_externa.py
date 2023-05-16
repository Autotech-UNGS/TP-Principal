import requests

class ConsumidorApiTecnicos():
    BASE_URL = "https://api-rest-pp1.onrender.com/api/usuarios/"

    @classmethod
    def consumir_tecnicos(cls, sucursal_supervisor):
        usuarios_data = requests.get(cls.BASE_URL)
        if usuarios_data.status_code != 200:
            raise requests.HTTPError({'message error' : usuarios_data.status_code})
        usuarios_data = usuarios_data.json()
        tecnicos = [{
            'id_empleado': tecnico['id_empleado'],
            'nombre_completo': tecnico['nombre_completo'],
            'dni': tecnico['dni'],
            'categoria': tecnico['categoria'],
            'branch': tecnico['branch']
        } for tecnico in usuarios_data if tecnico['branch'].endswith(sucursal_supervisor[-3:]) and tecnico['tipo'] == "Tecnico"]
        return tecnicos
    
    @classmethod
    def consumir_tecnico(cls, id_tecnico):
        url = f"{cls.BASE_URL}{id_tecnico}"
        tecnico_data = requests.get(url)
        if tecnico_data.status_code != 200:
            raise requests.HTTPError({'message error' : tecnico_data.status_code})
        tecnico_data = tecnico_data.json()
        if tecnico_data.get('tipo') != 'Tecnico':
            raise requests.HTTPError({'message error' : tecnico_data.status_code})
        return tecnico_data

    @classmethod
    def obtener_nombre_tecnico(cls, id_tecnico):
        tecnico_data = cls.consumir_tecnico(id_tecnico)
        nombre_tecnico = tecnico_data.get('nombre_completo')
        return nombre_tecnico

    @classmethod
    def obtener_categoria_tecnico(cls, id_tecnico):
        tecnico_data = cls.consumir_tecnico(id_tecnico)
        categoria_tecnico = tecnico_data.get('categoria')
        return categoria_tecnico

    @classmethod
    def obtener_taller_tecnico(cls, id_tecnico):
        tecnico_data = cls.consumir_tecnico(id_tecnico)
        taller_tecnico = tecnico_data.get('branch')
        return taller_tecnico
    
    @classmethod
    def obtener_id_tecnico(cls, id_tecnico):
        tecnico_data = cls.consumir_tecnico(id_tecnico)
        taller_tecnico = tecnico_data.get('id_empleado')
        return taller_tecnico