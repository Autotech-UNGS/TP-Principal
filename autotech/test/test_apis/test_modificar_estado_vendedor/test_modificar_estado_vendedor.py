from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller

class ModificarEstadosVendedor(TestSetUp):
    def post_response_aceptar_papeles(self, id_turno):
        url = reverse('aceptar-papeles', args=[id_turno])
        return self.client.post(url)
    
    def post_response_rechazar_papeles(self, id_turno):
        url = reverse('rechazar-papeles', args=[id_turno])
        return self.client.post(url)
    
    def test_aceptar_papeles(self):
        id_turno = 100
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 200)
        turno = Turno_taller.objects.get(id_turno = id_turno)
        self.assertDictEqual(turno.papeles_en_regla, True)
        
    def test_aceptar_estado_incorrecto(self):
        id_turno = 101
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 400)
        
    def test_aceptar_estado_rechazado(self):
        id_turno = 102
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 400)
        
    def test_aceptar_tipo_incorrecto_1(self):        
        id_turno = 103
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 400)
        
    def test_aceptar_tipo_incorrecto_2(self):
        id_turno = 104
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 400)
        
    def test_rechazar_papeles(self):
        id_turno = 200
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 200)
        turno = Turno_taller.objects.get(id_turno = id_turno)
        self.assertDictEqual(turno.papeles_en_regla, True)
        
    def test_aceptar_estado_incorrecto(self):
        id_turno = 201
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 400)
        
    def test_aceptar_tipo_incorrecto_1(self):        
        id_turno = 202
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 400)
        
    def test_aceptar_tipo_incorrecto_2(self):
        id_turno = 203
        self.assertEqual(self.post_response_aceptar_papeles(id_turno).status_code, 400)