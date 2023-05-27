from faker import Faker
from ddf import G
from rest_framework.test import APITestCase
from rest_framework import status
import pdb
from administracion.models import Turno_taller, Service, Registro_evaluacion_para_admin, Registro_extraordinario, Checklist_evaluacion
from administracion.models import Taller
from datetime import date, time
import json

class TestSetUp(APITestCase):
    def setUp(self):
        
        self.taller1 = G(Taller, id_taller=100, capacidad=10)
        self.taller3 = G(Taller,id_taller=101, capacidad=2)
        
        # vamos a saturar los horarios 8, 10 y 15 del taller 101, el dia 2023/06/27
        self.turno_test1 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,27), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,27), hora_fin=time(9,0,0))
        self.turno_test2 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,27), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,27), hora_fin=time(9,0,0))
        self.turno_test3 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,27), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,27), hora_fin=time(11,0,0))
        self.turno_test4 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,27), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,27), hora_fin=time(11,0,0))
        self.turno_test5 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,27), hora_inicio=time(15,0,0), fecha_fin=date(2023,6,27), hora_fin=time(16,0,0))
        self.turno_test6 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,27), hora_inicio=time(15,0,0), fecha_fin=date(2023,6,27), hora_fin=time(16,0,0))
        
        # vamos a saturar los horarios 8, 10, 13 y 15 del taller 101, el dia 2023/06/26, pero esta vez con turnos terminados/cancelados/rechazados/ausentes --> 
        # no debería afectar en nada a los test, porque los horarios siguen estando disponibles!
        self.turno_test7 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,26), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,26), hora_fin=time(9,0,0), estado='terminado')
        self.turno_test8 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,26), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,26), hora_fin=time(9,0,0), estado='terminado')
        self.turno_test9 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,26), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,26), hora_fin=time(11,0,0), estado='cancelado')
        self.turno_test10 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,26), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,26), hora_fin=time(11,0,0), estado='cancelado')
        self.turno_test11 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,26), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,26), hora_fin=time(14,0,0), estado='rechazado')
        self.turno_test12 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,26), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,26), hora_fin=time(14,0,0), estado='rechazado')
        self.turno_test13 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,26), hora_inicio=time(15,0,0), fecha_fin=date(2023,6,26), hora_fin=time(16,0,0), estado='ausente')
        self.turno_test14 = G(Turno_taller, taller_id = 101, fecha_inicio=date(2023,6,26), hora_inicio=time(15,0,0), fecha_fin=date(2023,6,26), hora_fin=time(16,0,0), estado='ausente')
        
        self.service1 = G(Service, id_service= 200, costo_base = 0.0, costo_total = 0.0, marca="generico", modelo = "generico", frecuencia_km=5000, duracion_total=180)
        
        # patente LCS262 es la evaluada
        self.turno_evaluacion = G(Turno_taller, id_turno = 400, taller_id = 101, patente = 'LCS262', tipo='evaluacion', estado="terminado")
        self.turno_extraordinario = G(Turno_taller, id_turno = 500, taller_id = 101, patente = 'LCS262', tipo='extraordinario', estado="terminado")
        # patente CBS291 es la no evaluada
        
        task = [10, 20]
        task_json = json.dumps(task)
        self.registro_evaluacion_admin = G(Registro_evaluacion_para_admin, id_turno=400, duracion_total_reparaciones=180, costo_total = 0.0)
        self.registro_extraordinario = G(Registro_extraordinario, id_tasks=task_json, id_turno=500)
        self.task_1 = G(Checklist_evaluacion, id_task=10, duracion_reemplazo=60, costo_reemplazo = 0.0)
        self.task_2 = G(Checklist_evaluacion, id_task=20, duracion_reemplazo=60, costo_reemplazo = 0.0)
        
        return super().setUp()
    
    def test_setup(self):
        pass        