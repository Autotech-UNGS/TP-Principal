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
        self.taller2 = G(Taller,id_taller=3)
        
        # asignado al 1 --> 8-9
        self.turno1 = G(Turno_taller, id_turno= 11, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,21), hora_fin=time(9,0,0), papeles_en_regla=True)
        
        # asignado al 1 --> 9-10
        self.turno2 = G(Turno_taller, id_turno= 12, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(9,0,0), fecha_fin=date(2023,9,21), hora_fin=time(10,0,0), papeles_en_regla=True)
        
        # asignado al 1 --> 10-11. No se puede reasignar
        self.turno3 = G(Turno_taller, id_turno= 13, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(11,0,0), papeles_en_regla=True)
        
        # 11-12, papeles no en regla
        self.turno4 = G(Turno_taller, id_turno= 14, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(11,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=False)
        
        # asignado al 1 --> 12-14. No podemos asignarle al 1 un turno de 12-13
        self.turno5 = G(Turno_taller, id_turno= 15, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(12,0,0), fecha_fin=date(2023,9,21), hora_fin=time(14,0,0), papeles_en_regla=True)
        self.turno6 = G(Turno_taller, id_turno= 16, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(12,0,0), fecha_fin=date(2023,9,21), hora_fin=time(13,0,0), papeles_en_regla=True)
        self.turno7 = G(Turno_taller, id_turno= 17, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(12,0,0), fecha_fin=date(2023,9,21), hora_fin=time(14,0,0), papeles_en_regla=True)
        self.turno8 = G(Turno_taller, id_turno= 18, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(13,0,0), fecha_fin=date(2023,9,21), hora_fin=time(14,0,0), papeles_en_regla=True)
        self.turno9 = G(Turno_taller, id_turno= 19, taller_id=1, tipo= 'evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(11,0,0), fecha_fin=date(2023,9,21), hora_fin=time(13,0,0), papeles_en_regla=True)
        
        # pertenece a otro taller. nadie puede hacerlo
        self.turno10 = G(Turno_taller, id_turno= 20, taller_id=3, tipo= 'evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(16,0,0), fecha_fin=date(2023,9,21), hora_fin=time(17,0,0), papeles_en_regla=True)

        return super().setUp()
    
    def test_setup(self):
        pass
