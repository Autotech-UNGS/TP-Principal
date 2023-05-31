from rest_framework.exceptions import ValidationError
from administracion.models import Taller
from talleres.api_client.cliente_sucursales import ClientSucursales
import re



class ValidadorTaller:
    

    def validar_taller(self, id_sucursal):
        
        taller_existente = Taller.objects.filter(id_sucursal = id_sucursal).exists()
        if taller_existente:
              raise ValidationError(f'Ya existe un taller para la sucursal {id_sucursal}') 

        return True
    
    def validar_datos(self, request):
        # id (sucursal),nombre, direccion, mail, telefono, capacidad, cant_tecnicos
        
        id_sucursal = request.data.get("id_sucursal")
        nombre = request.data.get("nombre")
        direccion =  request.data.get("direccion")
        mail =  request.data.get("mail")
        telefono =  request.data.get("telefono")
        capacidad =  request.data.get("capacidad")
        cant_tecnicos = request.data.get("cant_tecnicos")

        try:
            cliente = ClientSucursales.obtener_sucursal(id_sucursal)
        except Exception as e:
            error_messages = str(e)
            raise ValidationError(f'error: {error_messages}')
        
        if capacidad < 0:
             raise ValidationError(f'No se puede tener capacidad menor a 0 autos en el taller') 
        
        if cant_tecnicos < 0:
             raise ValidationError(f'No se puede no tener capacidad para técnicos') 
        
        if cant_tecnicos < capacidad:
             raise ValidationError(f'Debe de haber al menos, la misma cantidad de tecnicos que la capacidad de autos') 
             
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail):
            raise ValidationError('El correo electrónico no es válido')
        
        if not re.match(r'^\+?1?\d{9,15}$', telefono):
            raise ValidationError('El número de teléfono no es válido')
        
        if len(nombre) < 0 or len(nombre) > 30:
            raise ValidationError(f'El nombre debe tener entre 3 y 50 caracteres')
        
        if len(direccion) < 0 or len(direccion) > 30:
            raise ValidationError(f'La dirección debe tener entre 5 y 100 caracteres')
        
        if not isinstance(capacidad, int):
            raise ValidationError(f'La capacidad debe ser un número entero')
        
        if not isinstance(cant_tecnicos, int):
            raise ValidationError(f'La cantidad de técnicos debe ser un número entero')
        return True
    


    def validar_datos_reasignacion(self, request):
        # id (sucursal),nombre, direccion, mail, telefono, capacidad, cant_tecnicos
        
        id_sucursal_vieja = request.data.get("id_sucursal_vieja")
        id_sucursal_nueva = request.data.get("id_sucursal_nueva")
        

        try:
            cliente = ClientSucursales.obtener_sucursal(id_sucursal_vieja)
        except Exception as e:
            error_messages = str(e)
            raise ValidationError(f'error: {error_messages}')
        
        try:
            cliente = ClientSucursales.obtener_sucursal(id_sucursal_nueva)
        except Exception as e:
            error_messages = str(e)
            raise ValidationError(f'error: {error_messages}')
        
        
        return True
