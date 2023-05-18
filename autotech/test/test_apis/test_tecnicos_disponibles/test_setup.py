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
        
        # test 1 --> un tecnico disponible
        self.turno20 = G(Turno_taller, id_turno= 20, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 5, fecha_inicio=date(2023,5,27), hora_inicio=time(11,0,0), fecha_fin=date(2023,5,27), hora_fin=time(12,0,0))
        self.turno21 = G(Turno_taller, id_turno= 20, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,5,27), hora_inicio=time(11,0,0), fecha_fin=date(2023,5,27), hora_fin=time(12,0,0))
        
        # test 2 --> 0 tecnicos disponibles
        self.turno22 = G(Turno_taller, id_turno= 21, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 5, fecha_inicio=date(2023,5,21), hora_inicio=time(9,0,0), fecha_fin=date(2023,5,21), hora_fin=time(10,0,0))
        self.turno23 = G(Turno_taller, id_turno= 21, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 6, fecha_inicio=date(2023,5,21), hora_inicio=time(9,0,0), fecha_fin=date(2023,5,21), hora_fin=time(10,0,0))
        self.turno24 = G(Turno_taller, id_turno= 21, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,5,21), hora_inicio=time(9,0,0), fecha_fin=date(2023,5,21), hora_fin=time(10,0,0))
        
        # test 3 --> 2 tecnicos disponibles
        self.turno25 = G(Turno_taller, id_turno= 21, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,5,23), hora_inicio=time(13,0,0), fecha_fin=date(2023,5,23), hora_fin=time(14,0,0))
        
        return super().setUp()
    
    def test_setup(self):
        pass        