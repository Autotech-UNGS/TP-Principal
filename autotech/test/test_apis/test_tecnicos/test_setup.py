from ddf import G
from rest_framework.test import APITestCase
from administracion.models import Turno_taller, Taller

class TestSetUp(APITestCase):

    def setUp(self):
        # Instancias modelos
        self.taller = G(Taller, id_taller=1)      
        self.turno_taller = G(Turno_taller, tecnico_id=1, estado='en_proceso', taller_id=self.taller) # con id 1  
        self.turno_taller2 = G(Turno_taller, tecnico_id=1, estado='terminado', taller_id=self.taller) # con id 2
        
        self.assertEqual(self.taller, self.turno_taller.taller_id)
        self.assertEqual(Turno_taller.objects.count(), 2)
        self.assertEqual(self.turno_taller.estado, "en_proceso")
        self.assertEqual(self.turno_taller2.estado, "terminado")

        return super().setUp()
    
    def test_setup(self):
        pass