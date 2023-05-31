from faker import Faker
from ddf import G
from rest_framework.test import APITestCase
from administracion.models import Turno_taller
from administracion.models import Taller

class TestSetUp(APITestCase):
    def setUp(self):
        self.taller1 = G(Taller, id_taller=10, capacidad=20, estado=True)
        
        # Tiene que pasar de papeles_en_regla = False a papeles_en_regla = True
        self.turno_test_1_1 = G(Turno_taller, patente= "AAA100", taller_id=10, tipo='evaluacion', estado="pendiente", papeles_en_regla=False)
        # no pueden ser aceptados:
        self.turno_test_1_2 = G(Turno_taller, patente= "AAA101", taller_id=10, tipo='evaluacion', estado="rechazado", papeles_en_regla=False)
        self.turno_test_1_3 = G(Turno_taller, patente= "AAA102", taller_id=10, tipo='evaluacion', estado="en_proceso", papeles_en_regla=False)
        self.turno_test_1_4 = G(Turno_taller, patente= "AAA103", taller_id=10, tipo='service', estado="pendiente", papeles_en_regla=True)
        self.turno_test_1_5 = G(Turno_taller, patente= "AAA104", taller_id=10, tipo='service', estado="pendiente", papeles_en_regla=False)
        
        # Tiene que pasar de estado = 'pendiente' a estado = 'rechazado'
        self.turno_test_2_1 = G(Turno_taller, patente= "AAA200", taller_id=10, tipo='evaluacion', estado="pendiente", papeles_en_regla=False)
        # no pueden ser rechazados
        self.turno_test_2_2 = G(Turno_taller, patente= "AAA201", taller_id=10, tipo='evaluacion', estado="en_proceso", papeles_en_regla=False)        
        self.turno_test_2_3 = G(Turno_taller, patente= "AAA202", taller_id=10, tipo='service', estado="pendiente", papeles_en_regla=True)
        self.turno_test_2_4 = G(Turno_taller, patente= "AAA203", taller_id=10, tipo='service', estado="pendiente", papeles_en_regla=False)
        
        return super().setUp()
    
    def test_setup(self):
        pass