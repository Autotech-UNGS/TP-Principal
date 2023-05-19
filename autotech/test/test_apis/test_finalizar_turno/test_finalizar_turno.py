from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views import *
from test.factories.usuario_factorie import *

class FinalizarTurnoTestCase(TestSetUp):
    def post_response_finalizar_turno(self, id_turno: int):
        url = reverse('turnos-finalizar', args=[id_turno])
        return self.client.post(url)
        
    def get_response_turno_detalle(self, id_turno):
        url = reverse('turnos-detalle', args=[id_turno])
        return self.client.get(url)
    
    def generar_response_esperado(self, turno: Turno_taller):
        response_esperado ={
            'id_turno': turno.id_turno ,
            'tipo': turno.tipo,
            'estado': 'terminado',
            'taller_id': turno.taller_id.id_taller,
            'tecnico_id': turno.tecnico_id,
            'patente': turno.patente,
            'fecha_inicio': turno.fecha_inicio.strftime("%Y-%m-%d"),
            'hora_inicio': turno.hora_inicio.strftime("%H:%M:%S"),
            'fecha_fin': turno.fecha_fin.strftime("%Y-%m-%d"),
            'hora_fin': turno.hora_fin.strftime("%H:%M:%S"),
            'frecuencia_km': turno.frecuencia_km,
            'papeles_en_regla': turno.papeles_en_regla 
            }
        return response_esperado
    
    # ---------- en proceso ---------- #
    def test_en_proceso_evaluacion(self):
        turno = Turno_taller.objects.get(id_turno=2)
        response_esperado = self.generar_response_esperado(turno)
        
        self.assertEqual(self.post_response_finalizar_turno(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_turno_detalle(turno.id_turno).json(), response_esperado)
         
    def test_en_proceso_service(self):
        turno = Turno_taller.objects.get(id_turno=4)
        response_esperado = self.generar_response_esperado(turno)
        
        self.assertEqual(self.post_response_finalizar_turno(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_turno_detalle(turno.id_turno).json(), response_esperado)
        
    def test_en_proceso_reparacion(self):
        turno = Turno_taller.objects.get(id_turno=6)
        response_esperado = self.generar_response_esperado(turno)
        
        self.assertEqual(self.post_response_finalizar_turno(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_turno_detalle(turno.id_turno).json(), response_esperado)
    
    def test_en_proceso_extraordinario(self):
        turno = Turno_taller.objects.get(id_turno=8)
        response_esperado = self.generar_response_esperado(turno)

        self.assertEqual(self.post_response_finalizar_turno(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_turno_detalle(turno.id_turno).json(), response_esperado)        
        
    # ---------- pendiente ---------- #
    def test_pendiente_evaluacion(self):
        turno = Turno_taller.objects.get(id_turno=1)
        self.assertEqual(self.post_response_finalizar_turno(turno.id_turno).status_code, 400)
         
    def test_pendiente_service(self):
        turno = Turno_taller.objects.get(id_turno=3)
        self.assertEqual(self.post_response_finalizar_turno(turno.id_turno).status_code, 400)        
        
    def test_pendiente_reparacion(self):
        turno = Turno_taller.objects.get(id_turno=5)
        self.assertEqual(self.post_response_finalizar_turno(turno.id_turno).status_code, 400)
    
    def test_pendiente_extraordinario(self):
        turno = Turno_taller.objects.get(id_turno=7)
        self.assertEqual(self.post_response_finalizar_turno(turno.id_turno).status_code, 400)