from django.urls import reverse
from .test_setup import TestSetUp
from ddf import G
from administracion.models import Turno_taller, Registro_service
from administracion.models import Turno_taller
from datetime import date, time

class Garantias(TestSetUp):
    # vence el 10-06-2024 
    patente_con_garantia = "PPW289"
    # vence el 10-06-2025 
    patente_sin_garantia = "JWU991"
    
    def get_garantia_vigente(self, patente:str, fecha_turno:str, service_solicitado:int):
        url = reverse('garantia-vigente', args=[patente, fecha_turno, service_solicitado])
        return self.client.get(url)
    
    def get_estado_garantia(self, patente):
        url = reverse('estado-garantia', args=[patente])
        return self.client.get(url)
    
    def test_garantia_vigente(self):
        patente = self.patente_con_garantia
        response = self.get_garantia_vigente(patente, "2023-06-10", 22000)
        self.assertNotIn("no sigue en garantía", response.content.decode("utf-8"))
        
    def test_garantia_no_vigente(self):
        patente = self.patente_sin_garantia
        response = self.get_garantia_vigente(patente, "2024-10-11", 33000)
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
    
    def test_garantia_vencida(self):
        patente = self.patente_con_garantia
        response = self.get_garantia_vigente(patente, "2024-06-11", 22000)
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
           
    def test_garantia_al_limite(self):
        patente = self.patente_con_garantia
        response = self.get_garantia_vigente(patente, "2024-06-10", 22000)
        self.assertNotIn("no sigue en garantía", response.content.decode("utf-8"))
        
    def test_km_pasado(self):
        patente = self.patente_con_garantia
        response = self.get_garantia_vigente(patente, "2023-07-10", 40000) # tiene que tener un service mayor a 20k
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
        
          
    def test_km_al_limite(self):
        patente = self.patente_con_garantia
        
        turno_service1 =  G(Turno_taller, patente = patente, id_turno= 1, taller_id=10, tipo='service', estado="terminado", frecuencia_km = 5000, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        G(Registro_service, id_service=self.service1, id_turno=turno_service1)
        turno_service2 =  G(Turno_taller, patente = patente, id_turno= 2, taller_id=10, tipo='service', estado="terminado", frecuencia_km = 10000, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        G(Registro_service, id_service=self.service2, id_turno=turno_service2)
        
        response = self.get_garantia_vigente(patente, "2023-06-10", 32000) # tiene que tener un service de 15k y que no de error
        self.assertNotIn("no sigue en garantía", response.content.decode("utf-8"))
    
    def test_salteo_anteultimo_service(self):
        patente = self.patente_con_garantia
        response = self.get_garantia_vigente(patente, "2023-06-10", 32000) # hace el de 15 y no el de 5 ni el de 10
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
        
    def test_salteo_ultimo_service(self):
        patente = self.patente_con_garantia
        response = self.get_garantia_vigente(patente, "2023-06-10", 37000) # hace el de 10 y no el de 5
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
        
    def test_salteo_ultimo_service2(self):
        patente = self.patente_con_garantia
        turno_service1 =  G(Turno_taller, patente = patente, id_turno= 1, taller_id=10, tipo='service', estado="terminado", frecuencia_km = 5000, fecha_inicio=date(2023,9,21), hora_inicio=time(10,0,0), fecha_fin=date(2023,9,21), hora_fin=time(12,0,0), papeles_en_regla=True)
        G(Registro_service, id_service=self.service1, id_turno=turno_service1)
        response = self.get_garantia_vigente(patente, "2023-06-10", 32000) # hace el de 15 y no el de 10, pero si el de 5
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
           