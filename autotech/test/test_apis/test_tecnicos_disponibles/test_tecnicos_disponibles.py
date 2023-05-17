from unittest.mock import patch, Mock
from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views import *
from test.factories.usuario_factorie import *

class AsignarTecnicoTestCase(TestSetUp):
    id_tecnico = 2
    
    def get_response_tecnicos_disponibles(self, id_turno):
        url = reverse('tecnicos-disponibles', args=[id_turno])
        return self.client.get(url)
    
    def generar_response_esperado_asignar_tecnico(self, turno: Turno_taller):
        response_esperado ={
            'id_turno': turno.id_turno ,
            'tipo': turno.tipo,
            'estado': 'en_proceso',
            'taller_id': turno.taller_id.id_taller,
            'tecnico_id': self.id_tecnico,
            'patente': turno.patente,
            'fecha_inicio': turno.fecha_inicio.strftime("%Y-%m-%d"),
            'hora_inicio': turno.hora_inicio.strftime("%H:%M:%S"),
            'fecha_fin': turno.fecha_fin.strftime("%Y-%m-%d"),
            'hora_fin': turno.hora_fin.strftime("%H:%M:%S"),
            'frecuencia_km': 0,
            'papeles_en_regla': True 
            }
        return response_esperado
    
    # ------------------------ Tecnicos disponibles ------------------------ #
    def test_obtener_tecnico_disponible(self): 
        # el tecnico 1 esta disponible para hacer el turno 1
        turno = Turno_taller.objects.get(id_turno=1)
        self.assertEqual(self.get_response_tecnicos_disponibles(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_tecnicos_disponibles(turno.id_turno).json(), {'tecnicos_disponibles':[{'id_tecnico':1}]})
    
    def test_no_hay_tecnicos_disponibles(self): 
        # nadie puede hacer el turno 7, porque los 4,5 y 6 son a la vez
        turno = Turno_taller.objects.get(id_turno=1)
        self.assertEqual(self.get_response_tecnicos_disponibles(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_tecnicos_disponibles(turno.id_turno).json(), {'tecnicos_disponibles': [{'id_tecnico': 2}]})
    
    def test_obtener_tecnico_disponible(self):         
        turno = Turno_taller.objects.get(id_turno=1)
        response_esperado = [{'id_tecnico': 2}]
        
        self.assertEqual(self.get_response_tecnicos_disponibles(turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_tecnicos_disponibles(turno.id_turno).json(), {'tecnicos_disponibles': response_esperado})
    