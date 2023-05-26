from ddf import G
from rest_framework.test import APITestCase
from administracion.models import Turno_taller, Taller
from datetime import date, timedelta

class TestSetUp(APITestCase):

    def setUp(self):
        ayer = date.today() - timedelta(days=1)
        
        # Instancias modelos
        self.taller = G(Taller, id_taller=1)      
        self.turno_taller1 = G(Turno_taller, tipo='service', tecnico_id=None, estado='pendiente', taller_id=self.taller,papeles_en_regla=True ) # id 1
        self.turno_taller2 = G(Turno_taller, tipo='evaluacion', tecnico_id=None, estado='pendiente', taller_id=self.taller, papeles_en_regla=False) # id 2
        self.turno_taller3 = G(Turno_taller, tipo='evaluacion', tecnico_id=None, estado='pendiente', taller_id=self.taller, papeles_en_regla=True) # id 3
        self.turno_taller4 = G(Turno_taller, tipo='extraordinario', tecnico_id=None, estado='pendiente', taller_id=self.taller, papeles_en_regla=True) # id 4
        self.turno_taller5 = G(Turno_taller, tipo='reparacion', tecnico_id=None, estado='pendiente', taller_id=self.taller, papeles_en_regla=True) # id 5 

        self.turno_taller6 = G(Turno_taller, tipo='service', fecha_inicio = ayer, tecnico_id=1, estado='en_proceso', taller_id=self.taller, papeles_en_regla=True) # id 6
        self.turno_taller7 = G(Turno_taller, tipo='evaluacion', fecha_inicio = ayer, tecnico_id=1, estado='en_proceso', taller_id=self.taller,papeles_en_regla=True ) # id 7
        self.turno_taller8 = G(Turno_taller, tipo='extraordinario', fecha_inicio = ayer, tecnico_id=1, estado='en_proceso', taller_id=self.taller, papeles_en_regla=True) # id 8
        self.turno_taller9 = G(Turno_taller, tipo='reparacion', fecha_inicio = ayer, tecnico_id=1, estado='en_proceso', taller_id=self.taller, papeles_en_regla=True) # id 9

        self.turno_taller10 = G(Turno_taller, tecnico_id=1, estado='terminado', taller_id=self.taller, papeles_en_regla=True) # id 10   

        self.turno_taller11 = G(Turno_taller, tecnico_id=1, estado='cancelado', taller_id=self.taller, papeles_en_regla=True) # id 11 


        self.assertEqual(self.taller, self.turno_taller1.taller_id)
        
        self.assertEqual(Turno_taller.objects.count(), 11)

        self.assertEqual(Turno_taller.objects.filter(estado='pendiente').count(), 5)
        self.assertEqual(Turno_taller.objects.filter(estado='en_proceso').count(), 4)
        self.assertEqual(Turno_taller.objects.filter(estado='terminado').count(), 1)
        self.assertEqual(Turno_taller.objects.filter(estado='cancelado').count(), 1)

        self.assertEqual(self.turno_taller1.estado, 'pendiente')
        self.assertEqual(self.turno_taller7.estado, 'en_proceso')
        self.assertEqual(self.turno_taller10.estado, 'terminado')
        self.assertEqual(self.turno_taller11.estado, 'cancelado')

        return super().setUp()
    
    def test_setup(self):
        pass