"""
from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views.crear_turnos_views import *
from test.factories.usuario_factorie import *

class ReprogramarTurnoTestCase(TestSetUp):
    def post_response_reprogramar_turno(self, turno):
        url = reverse('reprogramar-turno')
        return self.client.post(url, turno, format='json')
    
# ------------------------------------------------------------------------------------------------ #    
# ------------------------------------- turno evaluacion: web ------------------------------------ #
# ------------------------------------------------------------------------------------------------ #    
    def test_turno_evaluacion_correcto(self):
        turno_correcto = {"patente": "AS123FD",
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "email": "luciacsoria5@gmail.com",
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": "AS123FD",
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-23",
                            "hora_fin": "13:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": False,
                            "taller_id": 10}
        
        response = self.post_response_reprogramar_turno(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)
        
    def test_turno_evaluacion_pendiente(self):
        
    def test_turno_evaluacion_rechazado(self):
        
    def test_turno_evaluacion_terminado(self):
        
    def test_turno_evaluacion_ausente(self):
        
    def test_turno_evaluacion_en_proceso(self):
        
        
        
    def test_turno_service_correcto(self):        
        
    def test_turno_extraordinario_correcto(self):
        
    def test_turno_reparacion_evaluacion_correcto(self):
        
    def test_turno_reparacion_extraordinario_correcto(self):
"""    