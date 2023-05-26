from administracion.models import Taller

def obtener_email_usuario():
    #return 'forozco@campus.ungs.edu.ar'
    return 'melaniiealbornoz@gmail.com'
    
def obtener_direccion_taller(taller_id) -> str:
    taller = Taller.objects.get(id_taller= taller_id)
    return f'{taller.direccion}, {taller.localidad}, {taller.provincia}.'