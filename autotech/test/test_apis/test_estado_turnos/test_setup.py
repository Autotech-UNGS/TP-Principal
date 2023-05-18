from ddf import G
from rest_framework.test import APITestCase
from administracion.models import Turno_taller, Taller

class TestSetUp(APITestCase):

    def setUp(self):
        # Instancias modelos
        self.taller = G(Taller, id_taller=1)      
        self.turno_taller1 = G(Turno_taller, tipo='service', tecnico_id=1, estado='pendiente', taller_id=self.taller) # id 1
        self.turno_taller2 = G(Turno_taller, tipo='evaluacion', tecnico_id=1, estado='pendiente', taller_id=self.taller, papeles_en_regla=False) # id 2
        self.turno_taller3 = G(Turno_taller, tipo='evaluacion', tecnico_id=1, estado='pendiente', taller_id=self.taller, papeles_en_regla=True) # id 3
        self.turno_taller4 = G(Turno_taller, tipo='extraordinario', tecnico_id=1, estado='pendiente', taller_id=self.taller) # id 4
        self.turno_taller5 = G(Turno_taller, tipo='reparacion', tecnico_id=1, estado='pendiente', taller_id=self.taller) # id 5 

        self.turno_taller6 = G(Turno_taller, tipo='service', tecnico_id=1, estado='en_proceso', taller_id=self.taller) # id 6
        self.turno_taller7 = G(Turno_taller, tipo='evaluacion', tecnico_id=1, estado='en_proceso', taller_id=self.taller) # id 7
        self.turno_taller8 = G(Turno_taller, tipo='extraordinario', tecnico_id=1, estado='en_proceso', taller_id=self.taller) # id 8
        self.turno_taller9 = G(Turno_taller, tipo='reparacion', tecnico_id=1, estado='en_proceso', taller_id=self.taller) # id 9

        self.turno_taller10 = G(Turno_taller, tecnico_id=1, estado='terminado', taller_id=self.taller) # id 10   


        self.assertEqual(self.taller, self.turno_taller1.taller_id)
        self.assertEqual(Turno_taller.objects.count(), 10)
        self.assertEqual(self.turno_taller1.estado, "pendiente")
        self.assertEqual(self.turno_taller7.estado, "en_proceso")

        return super().setUp()
    
    def test_setup(self):
        pass