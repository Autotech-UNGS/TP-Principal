from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller

class Garantias(TestSetUp):
    
    patente_con_garantia = ""
    patente_sin_garantia = ""
    patente_pruebas = "STT811"
    patente_salteo_services = "RTT102"
    
    def get_garantia_vigente(self, patente:str, fecha_turno:str, service_solicitado:int):
        url = reverse('garantia-vigente', args=[patente, fecha_turno, service_solicitado])
        return self.client.get(url)
    
    def get_estado_garantia(self, patente):
        url = reverse('estado-garantia', args=[patente])
        return self.client.get(url)
    
    def test_garantia_vigente(self):
        patente = self.patente_pruebas
        response = self.get_garantia_vigente(patente, "2023-06-10", 55000)
        self.assertNotIn("no sigue en garantía", response.content.decode("utf-8"))
        
    """
    def test_garantia_no_vigente(self):
        patente = self.patente_sin_garantia
        response = self.get_garantia_vigente(patente, "2023-06-10", 10000)
        self.assertEqual(response.status_code, 400)
    """           
    
    # no -> no existe un service con los datos especificados: 5000         
    def test_garantia_vencida(self):
        patente = self.patente_pruebas
        response = self.get_garantia_vigente(patente, "2023-06-13", 55000)
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
           
    # 200           
    def test_garantia_al_limite(self):
        patente = self.patente_pruebas
        response = self.get_garantia_vigente(patente, "2023-06-12", 55000)
        self.assertNotIn("no sigue en garantía", response.content.decode("utf-8"))
        
    # no
    def test_km_pasado(self):
        patente = self.patente_pruebas
        response = self.get_garantia_vigente(patente, "2023-06-10", 70000)
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
        
    # 200        
    def test_km_al_limite(self):
        patente = self.patente_pruebas
        response = self.get_garantia_vigente(patente, "2023-06-10", 55000)
        self.assertNotIn("no sigue en garantía", response.content.decode("utf-8"))
   
   # no -> no existe un service con los datos especificados: 10000     
    def test_salteo_anteultimo_service(self):
        patente = self.patente_salteo_services
        response = self.get_garantia_vigente(patente, "2023-06-10", 37000)
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))
        
    # no -> error: no existe un service con los datos especificados: 15000
    def test_salteo_ultimo_service(self):
        patente = self.patente_salteo_services
        response = self.get_garantia_vigente(patente, "2023-06-10", 32000)
        self.assertIn("no sigue en garantía", response.content.decode("utf-8"))