from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.crear_turnos_views import *
from test.factories.usuario_factorie import *

class CrearTurnoVendedorTestCase(TestSetUp):
    def post_response_crear_turno_vendedor(self, turno):
        url = reverse('crear-turno-vendedor')
        return self.client.post(url, turno, format='json')
    
    def test_cargar_turno_correcto_evaluacion_vendedor(self):
        turno_correcto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        response_esperado = {
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": None,
        "papeles_en_regla": True,
        "taller_id": 10}
    
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_correcto).status_code, 200)
        self.assertDictEqual(self.post_response_crear_turno_vendedor(turno_correcto).json(), response_esperado)

    def test_cargar_turno_correcto_service_vendedor(self):
        turno_correcto = {"id_turno": 8,
        "tipo": "service",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": 5000,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        response_esperado = {
        "tipo": "service",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": 5000,
        "taller_id": 10,
        "papeles_en_regla": True}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_correcto).status_code, 200)
        self.assertDictEqual(self.post_response_crear_turno_vendedor(turno_correcto).json(), response_esperado)
        
    def test_cargar_turno_correcto_extraordinario_vendedor(self):
        turno_correcto = {"id_turno": 9,
        "tipo": "extraordinario",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        response_esperado = {
        "tipo": "extraordinario",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "papeles_en_regla" : True}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_correcto).status_code, 200)
        self.assertDictEqual(self.post_response_crear_turno_vendedor(turno_correcto).json(), response_esperado)
        
    def test_cargar_turno_correcto_reparacion_vendedor(self):
        turno_correcto = {"id_turno": 10,
        "tipo": "reparacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        response_esperado = {
        "tipo": "reparacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "papeles_en_regla": True,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_correcto).status_code, 200)
        self.assertDictEqual(self.post_response_crear_turno_vendedor(turno_correcto).json(), response_esperado)
        
    def test_cargar_turno_para_ayer_vendedor(self):
        ayer = datetime.today() - timedelta(days=1)
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": ayer.strftime("%Y-%m-%d"),
        "hora_inicio": "10:00:00",
        "fecha_fin": ayer.strftime("%Y-%m-%d"),
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)
        
    def test_cargar_turno_para_hoy_vendedor(self):
        hoy = datetime.today()
        turno_correcto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": hoy.strftime("%Y-%m-%d"),
        "hora_inicio": "10:00:00",
        "fecha_fin": hoy.strftime("%Y-%m-%d"),
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        response_esperado = {
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": hoy.strftime("%Y-%m-%d"),
        "hora_inicio": "10:00:00",
        "fecha_fin": hoy.strftime("%Y-%m-%d"),
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "papeles_en_regla": True}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_correcto).status_code, 200)
        self.assertDictEqual(self.post_response_crear_turno_vendedor(turno_correcto).json(), response_esperado)
        
    def test_cargar_turno_para_mañana_vendedor(self):
        mañana = datetime.today() + timedelta(days=1)
        turno_correcto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": mañana.strftime("%Y-%m-%d"),
        "hora_inicio": "10:00:00",
        "fecha_fin": mañana.strftime("%Y-%m-%d"),
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        response_esperado = {
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": mañana.strftime("%Y-%m-%d"),
        "hora_inicio": "10:00:00",
        "fecha_fin": mañana.strftime("%Y-%m-%d"),
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "papeles_en_regla": True,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_correcto).status_code, 200)
        self.assertDictEqual(self.post_response_crear_turno_vendedor(turno_correcto).json(), response_esperado)       
    
    def test_service_sin_km_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "service",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)  
        
    def test_taller_no_existe_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "service",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": 0,
        "taller_id": 108,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)         
        
    def test_horarios_no_exactos_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:30:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:40:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)  
        
    def test_horarios_fuera_de_rango_superior_semana(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "15:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "18:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400) 
    
    def test_horarios_fuera_de_rango_inferior_semana_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "7:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "10:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400) 
        
        
    def test_horarios_fuera_de_rango_superior_domingo_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-22",
        "hora_inicio": "11:00:00",
        "fecha_fin": "2023-10-22",
        "hora_fin": "13:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)        
        
    def test_horarios_fuera_de_rango_inferior_domingo_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-22",
        "hora_inicio": "10:00:00",
        "fecha_fin": "2023-10-22",
        "hora_fin": "7:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)        
        
    def test_hora_inicio_y_final_iguales_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "11:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)
        
    def test_hora_inicio_superior_a_fin_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)
        
    def test_dia_inicio_superior_a_fin_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-22",
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "taller_id": 10,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)        
        
    def test_horario_no_disponible_completo_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-9-21",
        "hora_inicio": "10:00:00",
        "fecha_fin": "2023-9-21",
        "hora_fin": "12:00:00",
        "frecuencia_km": None,
        "taller_id": 11,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)        
        
    def test_horario_no_disponible_en_parte_vendedor(self):
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-9-21",
        "hora_inicio": "10:00:00",
        "fecha_fin": "2023-9-21",
        "hora_fin": "11:00:00",
        "frecuencia_km": 0,
        "taller_id": 11,
        "email": "luciacsoria5@gmail.com"}
        
        self.assertEqual(self.post_response_crear_turno_vendedor(turno_incorrecto).status_code, 400)       

         