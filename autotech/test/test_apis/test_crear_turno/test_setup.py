from faker import Faker
from ddf import G
from rest_framework.test import APITestCase
from rest_framework import status
import pdb
from administracion.models import Turno_taller
from administracion.models import Taller
from datetime import date, time

class TestSetUp(APITestCase):
    def setUp(self):
        self.taller1 = G(Taller, id_taller=10, capacidad=3)
        self.taller2 = G(Taller,id_taller=11, capacidad=2)
        
        # en el taller 10, no hay mas espacio a las 10 y 11 el dia 2023/9/21
        self.turno_test_1 = G(Turno_taller, id_turno= 1, taller_id=11, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        self.turno_test_2 = G(Turno_taller, id_turno= 2, taller_id=11, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        # este turno dura dos dias, viernes y sabado
        # sólo un lugar disponible el 2023/9/21 de 10 a 17
        # sólo un lugar disponible el 2023/9/22 de 8 a 12
        self.turno_test3 = G(Turno_taller, id_turno= 3, taller_id=10, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,22), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        # este turno dura dos dias, sabado y domingo
        # sólo un lugar disponible el 2023/9/23 de 10 a 17
        # sólo un lugar disponible el 2023/9/24 de 8 a 12
        self.turno_test4 = G(Turno_taller, id_turno= 4, taller_id=10, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,23), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,24), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        self.assertEqual(Turno_taller.objects.count(), 4)

        return super().setUp()
    
    def test_setup(self):
        pass