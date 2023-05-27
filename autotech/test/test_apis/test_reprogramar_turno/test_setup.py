"""
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
        self.taller1 = G(Taller, id_taller=10, capacidad=10)
        
        # evaluacion
        self.turno_evaluacion_valido1 = G(id_turno=100, tipo='evaluacion', estado='cancelado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=True)
        self.turno_evaluacion_valido2 = G(id_turno=101, tipo='evaluacion', estado='cancelado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        
        self.turno_evaluacion_invalido1 = G(id_turno=101, tipo='evaluacion', estado='pendiente', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        self.turno_evaluacion_invalido2 = G(id_turno=102, tipo='evaluacion', estado='rechazado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        self.turno_evaluacion_invalido3 = G(id_turno=103, tipo='evaluacion', estado='terminado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        self.turno_evaluacion_invalido4 = G(id_turno=104, tipo='evaluacion', estado='ausente', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        self.turno_evaluacion_invalido5 = G(id_turno=105, tipo='evaluacion', estado='en_proceso', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        
        # service
        self.turno_service_valido1 = G(id_turno=100, tipo='service', estado='cancelado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=True)
        
        self.turno_service_invalido1 = G(id_turno=101, tipo='service', estado='pendiente', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=True)
        self.turno_service_invalido2 = G(id_turno=102, tipo='service', estado='rechazado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=True)
        self.turno_service_invalido3 = G(id_turno=103, tipo='service', estado='terminado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=True)
        self.turno_service_invalido4 = G(id_turno=104, tipo='service', estado='ausente', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=True)
        self.turno_service_invalido5 = G(id_turno=105, tipo='service', estado='en_proceso', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=True)
        
        
        self.service1 = G(Service, id_service= 200, costo_base = 0.0, costo_total = 0.0, marca="generico", modelo = "generico", frecuencia_km=5000, duracion_total=180)
        self.service2 = G(Service, id_service= 300, costo_base = 0.0, costo_total = 0.0, marca="generico", modelo = "generico", frecuencia_km=10000, duracion_total=180)
        
        # la patente esa ya hizo el service de 5k
        self.turno_service = G(Turno_taller, patente = 'AS123FF', id_turno= 500, tipo='service', frecuencia_km= 5000, estado="terminado", tecnico_id= None, fecha_inicio=date(2023,4,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,4,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        self.registro_service = G(Registro_service, id_service=self.service1, id_turno=self.turno_service)
        
        # reparaciones:
        # esta patente tiene un turno de evaluacion, y también uno extraordinario:
        self.turno_evaluacion = G(Turno_taller, patente = 'LCS262', id_turno= 400, tipo='evaluacion', estado="terminado", fecha_inicio=date(2023,4,20), hora_inicio=time(10,0,0))
        self.turno_extraordinario = G(Turno_taller, patente = 'LCS262', id_turno= 401, tipo='extraordinario', estado="terminado", fecha_inicio=date(2023,4,20), hora_inicio=time(10,0,0))
        
        task = [10, 20]
        task_json = json.dumps(task)
        self.registro_evaluacion_admin = G(Registro_evaluacion_para_admin, id_turno=400, duracion_total_reparaciones=180, costo_total = 0.0)
        self.registro_extraordinario = G(Registro_extraordinario, id_tasks=task_json, id_turno=401)
        self.task_1 = G(Checklist_evaluacion, id_task=10, duracion_reemplazo=60, costo_reemplazo = 0.0)
        self.task_2 = G(Checklist_evaluacion, id_task=20, duracion_reemplazo=60, costo_reemplazo = 0.0)
        
        #self.assertEqual(Turno_taller.objects.count(), 15)

        return super().setUp()
    
    def test_setup(self):
        pass
"""        