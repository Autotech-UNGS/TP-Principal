from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views import *
from test.factories.usuario_factorie import *

class CrearTurnoTestCase(TestSetUp):
    def post_response_crear_turno(self, turno):
        url = reverse('turnos-create')
        return self.client.post(url, turno, format='json')
    
    def get_response_lista_turnos(self):
        url = reverse('turnos-list')
        return self.client.get(url)
        
    def get_response_turno_detalle(self, id_turno):
        url = reverse('turnos-detalle', args=[id_turno])
        return self.client.get(url)
    
    def test_cargar_turno_correcto_evaluacion(self):
        turno_correcto = {"id_turno": 20,
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
    
        self.assertEqual(self.post_response_crear_turno(turno_correcto).status_code, 200)
        
    def test_cargar_turno_correcto_service(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_correcto).status_code, 200)
        
    def test_cargar_turno_correcto_extraordinario(self):
        turno_correcto = {"id_turno": 9,
        "tipo": "extraordinario",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": 0,
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_correcto).status_code, 200)
        
    def test_cargar_turno_correcto_reparacion(self):
        turno_correcto = {"id_turno": 10,
        "tipo": "reparacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": "2023-10-23",
        "hora_inicio": "12:00:00",
        "fecha_fin": "2023-10-23",
        "hora_fin": "13:00:00",
        "frecuencia_km": 0,
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_correcto).status_code, 200)
        
    def test_cargar_turno_para_ayer(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)
        
    def test_cargar_turno_para_hoy(self):
        hoy = datetime.today()
        turno_incorrecto = {"id_turno": 6,
        "tipo": "evaluacion",
        "estado": "pendiente",
        "tecnico_id": None,
        "patente": "AS123FD",
        "fecha_inicio": hoy.strftime("%Y-%m-%d"),
        "hora_inicio": "10:00:00",
        "fecha_fin": hoy.strftime("%Y-%m-%d"),
        "hora_fin": "11:00:00",
        "frecuencia_km": None,
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)
        
    def test_cargar_turno_para_mañana(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_correcto).status_code, 200)       
    
    def test_service_sin_km(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)  
        
    def test_taller_no_existe(self):
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
        "papeles_en_regla": False,
        "taller_id": 108}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)         
        
    def test_horarios_no_exactos(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)  
        
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400) 
    
    def test_horarios_fuera_de_rango_inferior_semana(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400) 
        
        
    def test_horarios_fuera_de_rango_superior_domingo(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)        
        
    def test_horarios_fuera_de_rango_inferior_domingo(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)        
        
    def test_hora_inicio_y_final_iguales(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)
        
    def test_hora_inicio_superior_a_fin(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)
        
    def test_dia_inicio_superior_a_fin(self):
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
        "papeles_en_regla": False,
        "taller_id": 10}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)        
        
    def test_horario_no_disponible_completo(self):
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
        "papeles_en_regla": False,
        "taller_id": 11}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)        
        
    def test_horario_no_disponible_en_parte(self):
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
        "papeles_en_regla": False,
        "taller_id": 11}
        
        self.assertEqual(self.post_response_crear_turno(turno_incorrecto).status_code, 400)       

         