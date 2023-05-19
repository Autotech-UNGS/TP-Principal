from ddf import G
from rest_framework.test import APITestCase
from administracion.models import Turno_taller
from administracion.models import Taller
from datetime import date, time

class TestSetUp(APITestCase):
    def setUp(self):
        self.taller1 = G(Taller, id_taller=10, capacidad=10)
        
        self.turno_pendiente_evaluacion = G(Turno_taller, id_turno= 1, taller_id=10, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        self.turno_en_proceso_evaluacion = G(Turno_taller, id_turno= 2, taller_id=10, tipo='evaluacion', estado="en_proceso", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        self.turno_pendiente_service = G(Turno_taller, id_turno= 3, taller_id=10, tipo='service', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=False)
        self.turno_en_proceso_service = G(Turno_taller, id_turno= 4, taller_id=10, tipo='service', estado="en_proceso", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=False)
        
        self.turno_pendiente_reparacion = G(Turno_taller, id_turno= 5, taller_id=10, tipo='reparacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        self.turno_en_proceso_reparacion = G(Turno_taller, id_turno= 6, taller_id=10, tipo='reparacion', estado="en_proceso", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        self.turno_pendiente_extraordinario = G(Turno_taller, id_turno= 7, taller_id=10, tipo='extraordinario', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=False)
        self.turno_en_proceso_extraordinario = G(Turno_taller, id_turno= 8, taller_id=10, tipo='extraordinario', estado="en_proceso", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=False)
        
        
        
        self.assertEqual(Turno_taller.objects.count(), 8)

        return super().setUp()
    
    def test_setup(self):
        pass