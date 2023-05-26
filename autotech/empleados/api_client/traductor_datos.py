 
class TraductorDatosUsuarios():
    @classmethod  
    def traducir(cls, datos):
        diccionario_traduccion = {
            "id": "id",
            "fullName": "nombre_completo",
            "document": "dni",
            "username": "nombre_usuario",
            "type": "tipo",
            "branch": "branch",
            "technicalLevel": "categoria",
            "email": "email",
            "phoneCode": "codigo_telefono",
            "phoneNumber": "numero_telefono",
            "street": "calle",
            "streetNumber": "numero_calle",
            "city": "ciudad",
            "state": "provincia",
            "zipCode": "codigo_postal",
            "country": "pais"
        }

        datos_traducidos = []

        for dato in datos:
            dato_traducido = {}
            for clave, valor in dato.items():
                # si la clave no esta definida en el diccionario entonces devuelve por defecto la clave original
                clave_traducida = diccionario_traduccion.get(clave, clave)
                dato_traducido[clave_traducida] = valor
            datos_traducidos.append(dato_traducido)

        return datos_traducidos
    