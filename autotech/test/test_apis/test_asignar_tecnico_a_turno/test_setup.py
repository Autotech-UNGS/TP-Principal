from faker import Faker
from ddf import G
from rest_framework.test import APITestCase
from rest_framework import status
import pdb
from administracion.models import Turno_taller
from datetime import date, time

class TestSetUp(APITestCase):
    def setUp(self):
        # turnos del tecnico con id_empleado == 2
        self.turno1 = G(Turno_taller, id_turno= 1, tipo= 'Service', estado="Pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,21), hora_fin=time(9,0,0))
        self.turno2 = G(Turno_taller, id_turno= 2, tipo= 'Service', estado="Pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(13,0,0), fecha_fin=date(2023,9,21), hora_fin=time(14,0,0))
        self.turno3 = G(Turno_taller, id_turno= 3, tipo= 'Service', estado="Pendiente", tecnico_id= 2, fecha_inicio=date(2023,9,21), hora_inicio=time(16,0,0), fecha_fin=date(2023,9,21), hora_fin=time(17,0,0))
        
        # turnos para probar:
        turno_test_1 = G(Turno_taller, id_turno= 4, tipo='Evaluacion', estado="Pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        turno_test_2 = G(Turno_taller, id_turno= 5, tipo='Evaluacion', estado="Pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(13,0,0), papeles_en_regla=True)
        turno_test_3 = G(Turno_taller, id_turno= 6, tipo='Evaluacion', estado="Pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(13,0,0), papeles_en_regla=False)
        turno_test_4 = G(Turno_taller, id_turno= 7, tipo='Evaluacion', estado="Pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(13,0,0), fecha_fin=date(2023,9,21), hora_fin=time(14,0,0), papeles_en_regla=True)
        turno_test_5 = G(Turno_taller, id_turno= 8, tipo='Evaluacion', estado="Pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(12,0,0), fecha_fin=date(2023,9,21), hora_fin=time(15,0,0), papeles_en_regla=True)
        turno_test_6 = G(Turno_taller, id_turno= 9, tipo='Evaluacion', estado="Pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(15,0,0), fecha_fin=date(2023,9,21), hora_fin=time(17,0,0), papeles_en_regla=True)
        turno_test_7 = G(Turno_taller, id_turno= 10, tipo='Evaluacion', estado="Pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,21), hora_fin=time(10,0,0), papeles_en_regla=True)
    
        self.assertEqual(Turno_taller.objects.count(), 10)

        return super().setUp()
    
    def test_setup(self):
        pass
