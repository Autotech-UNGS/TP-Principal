import requests
from . import traductor_datos


class ClientTecnicos():
    # para obtener todos los tecnicos
    BASE_URL_TODOS = "https://gadmin-backend-production.up.railway.app/api/v1/user/getByType/TECNICO"
    # para obtener los tecnicos de un determinado taller
    BASE_URL_TALLER ="https://gadmin-backend-production.up.railway.app/api/v1/user/getByBranch"

    @classmethod
    def obtener_tecnicos(cls):
        response = cls._obtener_datos(cls.BASE_URL_TODOS)
        return response

    @classmethod
    def obtener_tecnicos_por_taller(cls, taller):
        url = f"{cls.BASE_URL_TALLER}/{taller}"
        response = cls._obtener_datos(url)
        return response

    @classmethod
    def _obtener_datos(cls, url):
        response = requests.get(url)

        if response.status_code != 200:
            raise requests.HTTPError({'message error': response.status_code})

        data = response.json()
        result = data.get("result")

        if result and "error" in result:
            error = result['error']
            errorCode = error.get('code')
            name = error.get('name')
            message = error.get('message')
            value = error.get('value')

            # Lanzar el error personalizado
            raise ValueError(f'Error al obtener los datos de los técnicos. Código: {errorCode}, Nombre: {name}, Mensaje: {message}, Valor: {value}')

        else:
            tecnicos_data = traductor_datos.TraductorDatosUsuarios.traducir(result)
            tecnicos_filtrados = [tecnico for tecnico in tecnicos_data if tecnico['tipo'] == 'TECNICO'] # unicamente tomamos los tipo TECNICO
            return tecnicos_filtrados
    
    
    @classmethod
    def obtener_datos_especificos_tecnicos(cls, taller):
        tecnicos_data = cls.obtener_tecnicos_por_taller(taller)
        tecnicos = [{
            'id': tecnico['id'],
            'nombre_completo': tecnico['nombre_completo'],
            'dni': tecnico['dni'],
            'categoria': tecnico['categoria'],
            'branch': tecnico['branch']
        } for tecnico in tecnicos_data if tecnico['branch'] == taller and tecnico['tipo'] == "TECNICO"]

        return tecnicos
    
    @classmethod
    def existe_tecnico(cls, id_tecnico):
        tecnicos = cls.obtener_tecnicos()
        existe = False
        for tecnico in tecnicos:
            existe = existe or (tecnico['id'] != id_tecnico)
        return existe
    
    @classmethod
    def obtener_tecnico(cls, id_tecnico):
        if cls.existe_tecnico(id_tecnico):
            tecnicos_data = cls.obtener_tecnicos()
            tecnico_data = {}
        
            for tecnico in tecnicos_data:
                if tecnico['id'] == id_tecnico:
                    tecnico_data = tecnico
            return tecnico_data
        else: 
            raise ValueError(f'Error el tecnico con {id_tecnico} no existe')
    
    @classmethod
    def obtener_nombre_tecnico(cls, id_tecnico):
        tecnico_data = cls.obtener_tecnico(id_tecnico)
        nombre_tecnico = tecnico_data.get('nombre_completo')
        return nombre_tecnico

    @classmethod
    def obtener_categoria_tecnico(cls, id_tecnico):
        tecnico_data = cls.obtener_tecnico(id_tecnico)
        categoria_tecnico = tecnico_data.get('categoria')
        return categoria_tecnico

    @classmethod
    def obtener_taller_tecnico(cls, id_tecnico):
        tecnico_data = cls.obtener_tecnico(id_tecnico)
        taller_tecnico = tecnico_data.get('branch')
        return taller_tecnico
    
    @classmethod
    def obtener_id_tecnico(cls, id_tecnico):
        tecnico_data = cls.obtener_tecnico(id_tecnico)
        taller_tecnico = tecnico_data.get('id')
        return taller_tecnico
            