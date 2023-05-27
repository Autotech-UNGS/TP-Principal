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
        self.taller2 = G(Taller,id_taller=101, capacidad=10)
        
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