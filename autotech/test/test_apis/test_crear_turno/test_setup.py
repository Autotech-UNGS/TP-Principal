from faker import Faker
from ddf import G
from rest_framework.test import APITestCase
from rest_framework import status
import pdb
from administracion.models import Turno_taller, Service, Registro_service, Registro_evaluacion_para_admin, Registro_extraordinario, Checklist_evaluacion
from administracion.models import Taller
from datetime import date, time
import json

class TestSetUp(APITestCase):
    def setUp(self):
        self.taller1 = G(Taller, id_taller=10, capacidad=3)
        self.taller2 = G(Taller,id_taller=11, capacidad=2)
        
        # en el taller 10, no hay mas espacio a las 10 y 11 el dia 2023/9/21
        self.turno_test_1 = G(Turno_taller, patente = 'AS123FD', id_turno= 1, taller_id=11, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        self.turno_test_2 = G(Turno_taller, id_turno= 2, taller_id=11, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        # este turno dura dos dias, viernes y sabado
        # sólo un lugar disponible el 2023/9/21 de 10 a 17
        # sólo un lugar disponible el 2023/9/22 de 8 a 12
        self.turno_test3 = G(Turno_taller, id_turno= 3, taller_id=10, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,22), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        # este turno dura dos dias, sabado y domingo
        # sólo un lugar disponible el 2023/9/23 de 10 a 17
        # sólo un lugar disponible el 2023/9/24 de 8 a 12
        self.turno_test4 = G(Turno_taller, id_turno= 4, taller_id=10, tipo='evaluacion', estado="pendiente", tecnico_id= None, fecha_inicio=date(2023,9,23), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,24), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        # estos turnos estan terminados/cancelados/rechazados/ausentes, asi que no hay problema para cargarles un turno encima
        # taller 10, a las 8, 10, 13 y 15hs, el 2023/09/29
        self.turno_test5 = G(Turno_taller, taller_id = 10, fecha_inicio=date(2023,9,29), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,29), hora_fin=time(9,0,0), estado='terminado')
        self.turno_test6 = G(Turno_taller, taller_id = 10, fecha_inicio=date(2023,9,29), hora_inicio=time(8,0,0), fecha_fin=date(2023,9,29), hora_fin=time(9,0,0), estado='terminado')
        self.turno_test7 = G(Turno_taller, taller_id = 10, fecha_inicio=date(2023,9,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,29), hora_fin=time(11,0,0), estado='cancelado')
        self.turno_test8 = G(Turno_taller, taller_id = 10, fecha_inicio=date(2023,9,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,29), hora_fin=time(11,0,0), estado='cancelado')
        self.turno_test9 = G(Turno_taller, taller_id = 10, fecha_inicio=date(2023,9,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,9,29), hora_fin=time(14,0,0), estado='rechazado')
        self.turno_test10 = G(Turno_taller, taller_id = 10, fecha_inicio=date(2023,9,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,9,29), hora_fin=time(14,0,0), estado='rechazado')
        self.turno_test11 = G(Turno_taller, taller_id = 10, fecha_inicio=date(2023,9,29), hora_inicio=time(15,0,0), fecha_fin=date(2023,9,29), hora_fin=time(16,0,0), estado='ausente')
        self.turno_test12 = G(Turno_taller, taller_id = 10, fecha_inicio=date(2023,9,29), hora_inicio=time(15,0,0), fecha_fin=date(2023,9,29), hora_fin=time(16,0,0), estado='ausente')
        
        
        self.service1 = G(Service, id_service= 200, costo_base = 0.0, costo_total = 0.0, marca="generico", modelo = "generico", frecuencia_km=5000, duracion_total=180)
        self.service2 = G(Service, id_service= 300, costo_base = 0.0, costo_total = 0.0, marca="generico", modelo = "generico", frecuencia_km=10000, duracion_total=180)
        
        # la patente esa ya hizo el service de 5k
        self.turno_service = G(Turno_taller, patente = 'AS123FF', id_turno= 500, tipo='service', frecuencia_km= 5000, estado="terminado", tecnico_id= None, fecha_inicio=date(2023,4,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,4,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        self.registro_service = G(Registro_service, id_service=self.service1, id_turno=self.turno_service)
        
        # reparaciones:
        # esta patente tiene un turno de evaluacion, y también uno extraordinario:
        self.turno_evaluacion = G(Turno_taller, patente = 'LCS262', id_turno= 400, tipo='evaluacion', estado="terminado", fecha_inicio=date(2023,4,20), hora_inicio=time(10,0,0))
        self.turno_extraordinario = G(Turno_taller, patente = 'LCS262', id_turno= 401, tipo='extraordinario', estado="terminado", fecha_inicio=date(2023,4,20), hora_inicio=time(10,0,0))
        
        task = ["10", "20"]
        #task_json = json.dumps(task)
        self.registro_evaluacion_admin = G(Registro_evaluacion_para_admin, id_turno=400, duracion_total_reparaciones=180, costo_total = 0.0)
        self.registro_extraordinario = G(Registro_extraordinario, id_tasks=task, id_turno=401)
        self.task_1 = G(Checklist_evaluacion, id_task="10", duracion_reemplazo=60, costo_reemplazo = 0.0)
        self.task_2 = G(Checklist_evaluacion, id_task="20", duracion_reemplazo=60, costo_reemplazo = 0.0)
        
        self.assertEqual(Turno_taller.objects.count(), 15)

        return super().setUp()
    
    def test_setup(self):
        pass