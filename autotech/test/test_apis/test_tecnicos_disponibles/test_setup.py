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
        self.taller1 = G(Taller, id_taller=1, capacidad=15)
        self.taller2 = G(Taller,id_taller=2)
        
        # los tecnicos 2 y 3 no pueden hacer el turno 1
        self.turno1 = G(Turno_taller, id_turno= 1, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,21), hora_fin=time(9,0,0))
        self.turno2 = G(Turno_taller, id_turno= 2, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,21), hora_fin=time(9,0,0))
        self.turno3 = G(Turno_taller, id_turno= 3, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 3, fecha_inicio=date(2023,9,21), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,21), hora_fin=time(9,0,0))
        
        # nadie puede hacer el turno 7
        self.turno4 = G(Turno_taller, id_turno= 4, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 1, fecha_inicio=date(2023,9,21), hora_inicio=time(9,0,0), fecha_fin=date(2023,9,21), hora_fin=time(10,0,0))
        self.turno5 = G(Turno_taller, id_turno= 5, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(9,0,0), fecha_fin=date(2023,9,21), hora_fin=time(10,0,0))
        self.turno6 = G(Turno_taller, id_turno= 6, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 3, fecha_inicio=date(2023,9,21), hora_inicio=time(9,0,0), fecha_fin=date(2023,9,21), hora_fin=time(10,0,0))
        self.turno7 = G(Turno_taller, id_turno= 7, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(9,0,0), fecha_fin=date(2023,9,21), hora_fin=time(10,0,0))
        
        # el tecnico 3 no puede hacer el turno 9
        self.turno8 = G(Turno_taller, id_turno= 8, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 3, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(11,0,0))
        self.turno9 = G(Turno_taller, id_turno= 9, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(11,0,0))
        
        return super().setUp()
    
    def test_setup(self):
        pass        