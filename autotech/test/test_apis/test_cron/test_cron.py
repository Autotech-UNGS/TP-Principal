from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views.crear_turnos_views import *
from test.factories.usuario_factorie import *

class EjecutarCronTestCase(TestSetUp):
    def post_ejecutar_cron(self):
        url = reverse('ejecutar-cron')
        return self.client.post(url)
    
    def test_cambian_a_ausente_1(self):
        #turno = Turno_taller.objects.get(id_turno = 200)
        self.assertEqual(self.post_ejecutar_cron().status_code, 200)
        turno_final = Turno_taller.objects.get(id_turno = 200)
        self.assertEqual(turno_final.estado, 'ausente')
        
    def test_cambian_a_ausente_2(self):
        #turno = Turno_taller.objects.get(id_turno = 201)
        self.assertEqual(self.post_ejecutar_cron().status_code, 200)
        turno_final = Turno_taller.objects.get(id_turno = 201)
        self.assertEqual(turno_final.estado, 'ausente')            
        
    def test_cambian_a_terminado_1(self):
        #turno = Turno_taller.objects.get(id_turno = 300)
        self.assertEqual(self.post_ejecutar_cron().status_code, 200)
        turno_final = Turno_taller.objects.get(id_turno = 300)
        self.assertEqual(turno_final.estado, 'terminado')
    
    def test_cambian_a_terminado_1(self):
        #turno = Turno_taller.objects.get(id_turno = 301)
        self.assertEqual(self.post_ejecutar_cron().status_code, 200)
        turno_final = Turno_taller.objects.get(id_turno = 301)
        self.assertEqual(turno_final.estado, 'terminado')
        
    def test_no_cambian_1(self):
        turno_inicial = Turno_taller.objects.get(id_turno = 400)
        estado1 = turno_inicial.estado
        self.assertEqual(self.post_ejecutar_cron().status_code, 200)
        turno_final = Turno_taller.objects.get(id_turno = 400)
        self.assertEqual(estado1, turno_final.estado)

    def test_no_cambian_2(self):
        turno_final = Turno_taller.objects.get(id_turno = 401)
        estado1 = turno_final.estado
        self.assertEqual(self.post_ejecutar_cron().status_code, 200)
        turno_final = Turno_taller.objects.get(id_turno = 401)
        self.assertEqual(estado1, turno_final.estado)        