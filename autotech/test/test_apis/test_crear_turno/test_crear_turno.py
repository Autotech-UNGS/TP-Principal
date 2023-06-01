from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views.crear_turnos_views import *
from test.factories.usuario_factorie import *

class CrearTurnoTestCase(TestSetUp):
    patente_cliente = "PPW825"
    patente_evaluada = "LCS262"
    patente_evaluacion = "ABC123"
    
    def post_response_crear_turno_evaluacion_web(self, turno):
        url = reverse('crear-turno-evaluacion-web')
        return self.client.post(url, turno, format='json')
    
    def post_response_crear_turno_evaluacion_presencial(self, turno):
        url = reverse('crear-turno-evaluacion-presencial')
        return self.client.post(url, turno, format='json')
    
    def post_response_crear_turno_service(self, turno):
        url = reverse('crear-turno-service')
        return self.client.post(url, turno, format='json')
    
    def post_response_crear_turno_reparacion(self, turno):
        url = reverse('crear-turno-reparacion')
        return self.client.post(url, turno, format='json')
    
    def post_response_crear_turno_extraordinario(self, turno):
        url = reverse('crear-turno-extraordinario')
        return self.client.post(url, turno, format='json')

    
# ------------------------------------------------------------------------------------------------ #    
# ------------------------------------- turno evaluacion: web ------------------------------------ #
# ------------------------------------------------------------------------------------------------ #    
    def test_evaluacion_web_correcto(self):
        turno_correcto = {"patente": self.patente_evaluacion,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-23",
                            "hora_fin": "13:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": False,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_evaluacion_web(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado) 
        
    def test_evaluacion_web_taller_no_existe(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "taller_id": 23}
        self.assertEqual(self.post_response_crear_turno_evaluacion_web(turno_incorrecto).status_code, 400)
        
    def test_evaluacion_web_taller_no_disponible_completo(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-9-21",
                            "hora_inicio": "10:00:00",
                            "taller_id": 11}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_web(turno_incorrecto).status_code, 400)        
        
    def test_evaluacion_web_taller_disponible_en_parte(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-9-21",
                            "hora_inicio": "10:00:00",
                            "taller_id": 11}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_web(turno_incorrecto).status_code, 400) 
        
    def test_evaluacion_web_horarios_no_exactos(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:30:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_web(turno_incorrecto).status_code, 400)   
    
    def test_evaluacion_web_horarios_fuera_de_rango_inferior_semana(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "7:00:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_web(turno_incorrecto).status_code, 400)       
        
    def test_evaluacion_web_horarios_fuera_de_rango_inferior_domingo(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-10-22",
                            "hora_inicio": "7:00:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_web(turno_incorrecto).status_code, 400)                

# ------------------------------------------------------------------------------------------------------- #        
# ------------------------------------- turno evaluacion: presencial ------------------------------------ #        
# ------------------------------------------------------------------------------------------------------- #
    def test_evaluacion_presencial_correcto(self):
        turno_correcto = {"patente": self.patente_evaluacion,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-23",
                            "hora_fin": "13:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_evaluacion_presencial(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado) 
        
    def test_evaluacion_presencial_taller_no_existe(self):
        turno_incorrecto = {"taller_id": 23,
                          "patente": self.patente_evaluacion,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00"}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_presencial(turno_incorrecto).status_code, 400)
        
    def test_evaluacion_presencial_taller_no_disponible_completo(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-9-21",
                            "hora_inicio": "10:00:00",
                            "taller_id": 11}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_presencial(turno_incorrecto).status_code, 400)        
        
    def test_evaluacion_presencial_taller_disponible_en_parte(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-9-21",
                            "hora_inicio": "10:00:00",
                            "taller_id": 11}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_presencial(turno_incorrecto).status_code, 400) 
        
    def test_evaluacion_presencial_horarios_no_exactos(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:30:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_presencial(turno_incorrecto).status_code, 400)   
    
    def test_evaluacion_presencial_horarios_fuera_de_rango_inferior_semana(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "7:00:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_presencial(turno_incorrecto).status_code, 400)       
        
    def test_evaluacion_presencial_horarios_fuera_de_rango_inferior_domingo(self):
        turno_incorrecto = {"patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-10-22",
                            "hora_inicio": "7:00:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_evaluacion_presencial(turno_incorrecto).status_code, 400)          
        
# ---------------------------------------------------------------------------------------- #        
# ------------------------------------- turno service ------------------------------------ #                
# ---------------------------------------------------------------------------------------- #
    def test_service_correcto(self):
        turno_correcto = {"patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "frecuencia_km": 25000,
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "service",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-23",
                            "hora_fin": "15:00:00",
                            "frecuencia_km": 10000,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_service(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado) 
        
    def test_service_correcto_2(self):
        turno_correcto = {"patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "frecuencia_km": 25000,
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "service",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-23",
                            "hora_fin": "15:00:00",
                            "frecuencia_km": 10000,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_service(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)  
        
    def test_service_correcto_3_dos_dias(self):
        turno_correcto = {"patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "16:00:00",
                          "frecuencia_km": 25000,
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "service",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "16:00:00",
                            "fecha_fin": "2023-10-24",
                            "hora_fin": "10:00:00",
                            "frecuencia_km": 10000,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_service(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)  
        
    def test_service_correcto_4_dos_dias_fin_de_mes(self):
        turno_correcto = {"patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-31",
                          "hora_inicio": "16:00:00",
                          "frecuencia_km": 25000,
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "service",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-31",
                            "hora_inicio": "16:00:00",
                            "fecha_fin": "2023-11-01",
                            "hora_fin": "10:00:00",
                            "frecuencia_km": 10000,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_service(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)                     
        
    def test_service_no_existe(self):
        turno_incorrecto = {"taller_id": 23,
                          "patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "frecuencia_km":15000}
        
        self.assertEqual(self.post_response_crear_turno_service(turno_incorrecto).status_code, 400)        
        
    def test_service_taller_no_existe(self):
        turno_incorrecto = {"taller_id": 103,
                          "patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "frecuencia_km": 25000}
        
        self.assertEqual(self.post_response_crear_turno_service(turno_incorrecto).status_code, 400)
        
    def test_service_taller_no_disponible_completo(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-9-21",
                            "hora_inicio": "10:00:00",
                            "taller_id": 11,
                            "frecuencia_km":25000}
        
        self.assertEqual(self.post_response_crear_turno_service(turno_incorrecto).status_code, 400)        
        
    def test_service_taller_disponible_en_parte(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-9-21",
                            "hora_inicio": "10:00:00",
                            "taller_id": 11,
                            "frecuencia_km":25000}
        
        self.assertEqual(self.post_response_crear_turno_service(turno_incorrecto).status_code, 400) 
        
    def test_service_horarios_no_exactos(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:30:00",
                            "frecuencia_km":25000,
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_service(turno_incorrecto).status_code, 400)   
    
    def test_service_horarios_fuera_de_rango_inferior_semana(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "7:00:00",
                            "frecuencia_km":25000,
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_service(turno_incorrecto).status_code, 400)       
        
    def test_service_horarios_fuera_de_rango_inferior_domingo(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-22",
                            "hora_inicio": "7:00:00",
                            "frecuencia_km":25000,
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_service(turno_incorrecto).status_code, 400)                  
        
# ------------------------------------------------------------------------------------------- #            
# ------------------------------------- turno reparacion ------------------------------------ #            
# ------------------------------------------------------------------------------------------- #                
    def test_reparacion_evaluacion_correcto(self):
        turno_correcto = {"patente": self.patente_evaluada,
                          "fecha_inicio": "2023-10-24",
                          "hora_inicio": "12:00:00",
                          "taller_id": 10,
                          "origen": "evaluacion"}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "reparacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_evaluada,
                            "fecha_inicio": "2023-10-24",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-24",
                            "hora_fin": "15:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": True,
                            "taller_id": 10}      
        
        response = self.post_response_crear_turno_reparacion(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)  
    
    def test_reparacion_extraordinario_correcto(self):   
        turno_correcto = {"patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-24",
                          "hora_inicio": "12:00:00",
                          "taller_id": 10,
                          "origen": "extraordinario"}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "reparacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-24",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-24",
                            "hora_fin": "14:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_reparacion(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)  
        
    def test_reparacion_evaluacion_patente_no_evaluada(self):
        turno_incorrecto = {"patente": "262CBS",
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "taller_id": 10,
                          "origen": "evaluacion"}
        
        self.assertEqual(self.post_response_crear_turno_reparacion(turno_incorrecto).status_code, 400)        
    
    def test_reparacion_extraordinario_patente_no_evaluada(self):    
        turno_incorrecto = {"patente": "262CBS",
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "taller_id": 10,
                          "origen": "extraordinario"}              
        
        self.assertEqual(self.post_response_crear_turno_reparacion(turno_incorrecto).status_code, 400)        

# ----------------------------------------------------------------------------------------------- #    
# ------------------------------------- turno extraordinario ------------------------------------ #    
# ----------------------------------------------------------------------------------------------- #                        
    def test_extraordinario_correcto(self):
        turno_correcto = {"patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "extraordinario",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:00:00",
                            "fecha_fin": "2023-10-23",
                            "hora_fin": "13:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": True,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_extraordinario(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado) 
        
    def test_extraordinario_taller_no_existe(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                          "fecha_inicio": "2023-10-23",
                          "hora_inicio": "12:00:00",
                          "taller_id": 23}
        self.assertEqual(self.post_response_crear_turno_extraordinario(turno_incorrecto).status_code, 400)
        
    def test_extraordinario_taller_no_disponible_completo(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-9-21",
                            "hora_inicio": "10:00:00",
                            "taller_id": 11}
        
        self.assertEqual(self.post_response_crear_turno_extraordinario(turno_incorrecto).status_code, 400)        
        
    def test_extraordinario_taller_disponible_en_parte(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-9-21",
                            "hora_inicio": "10:00:00",
                            "taller_id": 11}
        
        self.assertEqual(self.post_response_crear_turno_extraordinario(turno_incorrecto).status_code, 400) 
        
    def test_extraordinario_horarios_no_exactos(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "12:30:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_extraordinario(turno_incorrecto).status_code, 400)   
    
    def test_extraordinario_horarios_fuera_de_rango_inferior_semana(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-23",
                            "hora_inicio": "7:00:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_extraordinario(turno_incorrecto).status_code, 400)       
        
    def test_extraordinario_horarios_fuera_de_rango_inferior_domingo(self):
        turno_incorrecto = {"patente": self.patente_cliente,
                            "fecha_inicio": "2023-10-22",
                            "hora_inicio": "7:00:00",
                            "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_extraordinario(turno_incorrecto).status_code, 400)                
        
# ----------------------------------------------------------------------------------------------- #    
# ------------------------ extra: turnos en horarios con turnos inválidos ----------------------- #    
# ----------------------------------------------------------------------------------------------- #         
    def test_turno_sobre_terminado(self):
        turno_correcto = {"patente": self.patente_evaluacion,
                          "fecha_inicio": "2023-9-29",
                          "hora_inicio": "08:00:00",
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-09-29",
                            "hora_inicio": "08:00:00",
                            "fecha_fin": "2023-09-29",
                            "hora_fin": "09:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": False,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_evaluacion_web(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado) 
        
    def test_turno_sobre_cancelado(self):
        turno_correcto = {"patente": self.patente_evaluacion,
                          "fecha_inicio": "2023-9-29",
                          "hora_inicio": "10:00:00",
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-09-29",
                            "hora_inicio": "10:00:00",
                            "fecha_fin": "2023-09-29",
                            "hora_fin": "11:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": False,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_evaluacion_web(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)         
        
    def test_turno_sobre_rechazado(self):
        turno_correcto = {"patente": self.patente_evaluacion,
                          "fecha_inicio": "2023-9-29",
                          "hora_inicio": "13:00:00",
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-09-29",
                            "hora_inicio": "13:00:00",
                            "fecha_fin": "2023-09-29",
                            "hora_fin": "14:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": False,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_evaluacion_web(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)         
        
    def test_turno_sobre_ausente(self):
        turno_correcto = {"patente": self.patente_evaluacion,
                          "fecha_inicio": "2023-9-29",
                          "hora_inicio": "15:00:00",
                          "taller_id": 10}
        
        response_esperado = { "id_turno": 501,
                            "tipo": "evaluacion",
                            "estado": "pendiente",
                            "tecnico_id": None,
                            "patente": self.patente_evaluacion,
                            "fecha_inicio": "2023-09-29",
                            "hora_inicio": "15:00:00",
                            "fecha_fin": "2023-09-29",
                            "hora_fin": "16:00:00",
                            "frecuencia_km": None,
                            "papeles_en_regla": False,
                            "taller_id": 10}
        
        response = self.post_response_crear_turno_evaluacion_web(turno_correcto)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)
        