from administracion.models import Turno_taller, Registro_reparacion
from django.core.exceptions import ObjectDoesNotExist

class ValidadorTurno():

    def existe_turno(self, turno):
        try:
            Turno_taller.objects.get(id=turno.id)
            return True
        except ObjectDoesNotExist:
            return False
    
    def es_turno_evaluacion(self, turno):
        return turno.tipo == 'evaluacion'
    
    def es_turno_extraordinario(self, turno):
        return turno.tipo == 'extraordinario'
    
    
class ValidadorRegistroReparacion():
    
    def existe_registro_reparacion(self, id_turno):
        try:
            turno = Turno_taller.objects.get(id_turno=id_turno)
            Registro_reparacion.objects.get(id_turno=turno)
            return True
        except ObjectDoesNotExist:
            return False

