import requests
from . import traductor_datos


class ClientSupervisor():
    # para obtener todos los tecnicos
    BASE_URL_TODOS = "https://gadmin-backend-production.up.railway.app/api/v1/user/getByType/SUPERVISOR_TECNICO"
    # para obtener los tecnicos de un determinado taller
    BASE_URL_SUCURSAL ="https://gadmin-backend-production.up.railway.app/api/v1/user/getByBranch"

    @classmethod
    def obtener_supervisores(cls):
        response = cls._obtener_datos(cls.BASE_URL_TODOS)
        return response

    @classmethod
    def obtener_supervisor_por_branch(cls, sucursal):
        url = f"{cls.BASE_URL_SUCURSAL}/{sucursal}"
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
            error = result["error"]
            errorCode = error.get("code")
            name = error.get("name")
            message = error.get("message")
            value = error.get("value")

            # Lanzar el error personalizado
            raise ValueError(f"Error al obtener los datos de los Supervisores. Código: {errorCode}, Nombre: {name}, Mensaje: {message}, Valor: {value}")

        else:
            supervisor_data = traductor_datos.TraductorDatosUsuarios.traducir(result)
            supervisores_filtrados = [supervisor for supervisor in supervisor_data if supervisor['tipo'] == 'SUPERVISOR_TECNICO'] # unicamente tomamos los tipo SUPERVISOR_TECNICO
            return supervisores_filtrados
   
    @classmethod
    def existe_supervisor(cls, id_supervisor):
        supervisores = cls.obtener_supervisores()
        existe = False
        for supervisor in supervisores:
            existe = existe or (supervisor['id'] != id_supervisor)
        return existe

    @classmethod
    def obtener_supervisor(cls, id_supervisor):
        if cls.existe_supervisor(id_supervisor):
            supervisores_data = cls.obtener_supervisores()
            supervisor_data = {}
        
            for supervisor in supervisores_data:
                if supervisor['id'] == id_supervisor:
                    supervisor_data = supervisor
            return supervisor_data
        else: 
            raise ValueError(f'Error el supervisor con id: {id_supervisor} no existe')