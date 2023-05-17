from unittest.mock import patch, Mock
from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views import *
from test.factories.usuario_factorie import *

class TecnicosDisponibles(TestSetUp):
    
    def get_response_tecnicos_disponibles(self, id_turno):
        url = reverse('tecnicos-disponibles', args=[id_turno])
        return self.client.get(url)
    
    # ------------------------ Tecnicos disponibles ------------------------ #
    
    # en el taller 1 tenemos los tecnicos 4,5 y 6
    
    # el turno 7 esta signado al tecnico 4. Le asignamos un turno igual al tecnico 5. 
    # Entonces, el 6 es el unico libre a esa hora --> turno21
    def test_obtener_tecnico_disponible(self): 
        turno = Turno_taller.objects.get(id_turno=21)
        self.assertEqual(self.get_response_tecnicos_disponibles(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_tecnicos_disponibles(turno.id_turno).json(), {'tecnicos_disponibles':[{'id_tecnico':6}]})
    
    # el turno 8 esta signado al tecnico 4. Le asignamos un turno igual al tecnico 5 y otro al tecnico 6. 
    # Entonces, nadie esta libre para hacer el turno24
    def test_no_hay_tecnicos_disponibles(self): 
        turno = Turno_taller.objects.get(id_turno=24)
        self.assertEqual(self.get_response_tecnicos_disponibles(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_tecnicos_disponibles(turno.id_turno).json(), {'tecnicos_disponibles': []})
    
    # el turno 17 esta asignado al tecnico 4.
    # Entonces, el 5 y el 6 pueden hacer el turno 25
    def test_obtener_tecnico_disponible(self):         
        turno = Turno_taller.objects.get(id_turno=25)
        response_esperado = [{'id_tecnico': 5}], {'id_tecnico': 6}
        
        self.assertEqual(self.get_response_tecnicos_disponibles(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_tecnicos_disponibles(turno.id_turno).json(), {'tecnicos_disponibles': response_esperado})
    