from administracion.models import Turno_taller, Registro_reparacion
from django.core.exceptions import ObjectDoesNotExist

class ValidadorTurno():

    def existe_turno(self, turno):
        try:
            Turno_taller.objects.get(id_turno=turno.id_turno)
            return True
        except ObjectDoesNotExist:
            return False
    

class ValidadorRegistroReparacion():
    
    def existe_registro_reparacion(self, id_turno):
        try:
            turno = Turno_taller.objects.get(id_turno=id_turno)
            Registro_reparacion.objects.get(id_turno=turno)
            return True
        except ObjectDoesNotExist:
            return False

