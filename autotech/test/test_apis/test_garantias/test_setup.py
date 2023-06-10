from faker import Faker
from ddf import G
from rest_framework.test import APITestCase
from administracion.models import Turno_taller, Service, Registro_service
from administracion.models import Taller
from datetime import date, time

class TestSetUp(APITestCase):
    def setUp(self):
        self.patente_salteo_services = "RTT102"
        self.taller1 = G(Taller, id_taller=10, capacidad=3, estado=True)
        
        self.turno_service =  G(Turno_taller, patente = self.patente_salteo_services, id_turno= 1, taller_id=10, tipo='service', estado="terminado", frecuencia_km = 5000, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        
        self.service1 = G(Service, id_service= 200, costo_base = 20.0, costo_total = 20.0, marca="generico", modelo = "generico", frecuencia_km=5000, duracion_total=180, activo=True)
        self.registro_service = G(Registro_service, id_service=self.service1, id_turno=self.turno_service)
        
        self.service2 = G(Service, id_service= 201, costo_base = 20.0, costo_total = 20.0, marca="generico", modelo = "generico", frecuencia_km=10000, duracion_total=180, activo=True)
        self.service3 = G(Service, id_service= 202, costo_base = 20.0, costo_total = 20.0, marca="generico", modelo = "generico", frecuencia_km=15000, duracion_total=180, activo=True)
        self.service4 = G(Service, id_service= 203, costo_base = 20.0, costo_total = 20.0, marca="generico", modelo = "generico", frecuencia_km=20000, duracion_total=180, activo=True)
        
        return super().setUp()
    
    def test_setup(self):
        pass        