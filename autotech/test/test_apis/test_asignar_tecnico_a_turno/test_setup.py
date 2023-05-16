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
        
        # turnos del tecnico con id_empleado == 2
        self.turno1 = G(Turno_taller, id_turno= 1, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,21), hora_fin=time(9,0,0))
        self.turno2 = G(Turno_taller, id_turno= 2, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(13,0,0), fecha_fin=date(2023,9,21), hora_fin=time(14,0,0))
        self.turno3 = G(Turno_taller, id_turno= 3, taller_id=1, tipo= 'service', estado="pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(16,0,0), fecha_fin=date(2023,9,21), hora_fin=time(17,0,0))
        
        # turnos para probar:
        self.turno_test_1 = G(Turno_taller, id_turno= 4, taller_id=1, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        self.turno_test_2 = G(Turno_taller, id_turno= 5, taller_id=1, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(13,0,0), papeles_en_regla=True)
        self.turno_test_3 = G(Turno_taller, id_turno= 6, taller_id=1, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(13,0,0), papeles_en_regla=False)
        self.turno_test_4 = G(Turno_taller, id_turno= 7, taller_id=1, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(13,0,0), fecha_fin=date(2023,9,21), hora_fin=time(14,0,0), papeles_en_regla=True)
        self.turno_test_5 = G(Turno_taller, id_turno= 8, taller_id=1, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(12,0,0), fecha_fin=date(2023,9,21), hora_fin=time(15,0,0), papeles_en_regla=True)
        self.turno_test_6 = G(Turno_taller, id_turno= 9, taller_id=1, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(15,0,0), fecha_fin=date(2023,9,21), hora_fin=time(17,0,0), papeles_en_regla=True)
        self.turno_test_7 = G(Turno_taller, id_turno= 10, taller_id=1, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,21), hora_fin=time(10,0,0), papeles_en_regla=True)
        self.turno_test_8 = G(Turno_taller, id_turno= 11, taller_id=2, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(11,0,0), papeles_en_regla=True)
    
        self.assertEqual(Turno_taller.objects.count(), 11)

        return super().setUp()
    
    def test_setup(self):
        pass
