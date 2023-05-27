from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller

class ModificarEstadosVendedor(TestSetUp):
    def post_response_aceptar_papeles(self, patente):
        url = reverse('aceptar-papeles', args=[patente])
        return self.client.post(url)
    
    def post_response_rechazar_papeles(self, patente):
        url = reverse('rechazar-papeles', args=[patente])
        return self.client.post(url)
    
    def test_aceptar_papeles(self):
        patente = "AAA100"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 200)
        turno = Turno_taller.objects.get(patente = patente)
        self.assertEqual(turno.papeles_en_regla, True)
        
    def test_aceptar_estado_incorrecto(self):
        patente = "AAA101"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 400)
        
    def test_aceptar_estado_rechazado(self):
        patente = "AAA102"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 400)
        
    def test_aceptar_tipo_incorrecto_1(self):        
        patente = "AAA103"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 400)
        
    def test_aceptar_tipo_incorrecto_2(self):
        patente = "AAA104"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 400)
        
    def test_rechazar_papeles(self):
        patente = "AAA200"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 200)
        turno = Turno_taller.objects.get(patente = patente)
        self.assertEqual(turno.papeles_en_regla, True)
        
    def test_aceptar_estado_incorrecto(self):
        patente = "AAA201"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 400)
        
    def test_aceptar_tipo_incorrecto_1(self):        
        patente = "AAA202"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 400)
        
    def test_aceptar_tipo_incorrecto_2(self):
        patente = "AAA203"
        self.assertEqual(self.post_response_aceptar_papeles(patente).status_code, 400)