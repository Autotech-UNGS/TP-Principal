from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views.crear_turnos_views import *
from test.factories.usuario_factorie import *

class ReprogramarTurnoTestCase(TestSetUp):
    def post_response_reprogramar_turno(self, turno):
        url = reverse('reprogramar-turno')
        return self.client.post(url, turno, format='json')
    
# ------------------------------------- turno evaluacion ------------------------------------ #
    # papeles en regla
    def test_turno_evaluacion_correcto(self):
        turno_correcto = {"id_turno": 100,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        response_esperado = { "id_turno": 301,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": "ABC111",
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-23",
                            "hora_fin": "13:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_reprogramar_turno(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)
        
    # papeles no en regla        
    def test_turno_evaluacion_correcto_2(self):
        turno_correcto = {"id_turno": 101,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        response_esperado = { "id_turno": 301,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": "ABC112",
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
        turno_incorrecto = {"id_turno": 102,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)
        
    def test_turno_evaluacion_rechazado(self):
        turno_incorrecto = {"id_turno": 103,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)
        
    def test_turno_evaluacion_terminado(self):
        turno_incorrecto = {"id_turno": 104,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)
        
    def test_turno_evaluacion_ausente(self):
        turno_incorrecto = {"id_turno": 105,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)
        
    def test_turno_evaluacion_en_proceso(self):
        turno_incorrecto = {"id_turno": 106,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)
        
# ------------------------------------- turno service ------------------------------------ #        

    def test_turno_service_correcto(self):        
        turno_correcto = {"id_turno": 200,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        response_esperado = { "id_turno": 301,
                            "tipo": "service",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": "ABC118",
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-23",
                            "hora_fin": "14:00:00",
                            "frecuencia_km": 5000,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_reprogramar_turno(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)
        
    # turno que dura dos dias
    def test_turno_service_correcto_2(self):        
        turno_correcto = {"id_turno": 200,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "16:00:00"} 
        
        response_esperado = { "id_turno": 301,
                            "tipo": "service",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": "ABC118",
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "16:00:00",
                            "fecha_fin": "2023-10-24",
                            "hora_fin": "09:00:00",
                            "frecuencia_km": 5000,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_reprogramar_turno(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado) 
        
    def test_turno_service_horarios_incorrectos(self):    
        turno_incorrecto = {"id_turno": 200,
                          "fecha_inicio": "2023-06-29",
                          "hora_inicio": "16:00:00"} # no hay lugar el 2023/06/30 a las 8 
        
        response = self.post_response_reprogramar_turno(turno_incorrecto)
        self.assertEqual(response.status_code, 400)      
        
    def test_turno_service_horarios_incorrectos_2(self):        
        turno_incorrecto = {"id_turno": 200,
                          "fecha_inicio": "2023-06-30",
                          "hora_inicio": "08:00:00"} # no hay lugar el 2023/06/30 a las 8 
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)   
                      
                      
    def test_turno_patente_invalida_mismo_tipo(self):
        turno_incorrecto = {"id_turno": 117,
                          "fecha_inicio": "2023-10-16",
                          "hora_inicio": "08:00:00"}
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)   
    
    def test_turno_patente_invalida_mismo_tipo(self):
        turno_incorrecto = {"id_turno": 117,
                          "fecha_inicio": "2023-10-16",
                          "hora_inicio": "15:00:00"}
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)   
        
    def test_patente_invalida_mismo_dia_horario(self):
        turno_incorrecto = {"id_turno": 117,
                          "fecha_inicio": "2023-10-17",
                          "hora_inicio": "8:00:00"}
        
        self.assertEqual(self.post_response_reprogramar_turno(turno_incorrecto).status_code, 400)   

    """
    def test_patente_valida_mismo_dia_horario_distinto_horario(self):
        turno_correcto = {"id_turno": 117,
                          "fecha_inicio": "2023-10-17",
                          "hora_inicio": "11:00:00"}
        
        response_esperado = { "id_turno": 301,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": "FRN198",
                            "fecha_inicio": "2023-10-17",
                            "hora_inicio": "11:00:00",
                            "fecha_fin": "2023-10-17",
                            "hora_fin": "12:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_reprogramar_turno(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)  
    """       
        
        