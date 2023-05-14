from unittest.mock import patch, Mock
from django.urls import reverse
from .test_setup import TestSetUp
#from test.factories.tecnicos_factories import UsuarioFactory
#from test.factories.turnos_factories import TurnoFactory
from administracion.models import Turno_taller
from turnos.views import *

class AsignarTecnicoTestCase(TestSetUp):
    id_tecnico = 2
    def get_response_lista_turnos(self):
        url = reverse('turnos-list')
        return self.client.get(url)
        
    def get_response_turno_detalle(self, id_turno):
        url = reverse('turnos-detalle', args=[id_turno])
        return self.client.get(url)
        
    def post_response_asignar_tecnico(self, id_tecnico, id_turno):
        url = reverse('asignar-tecnico', args=[id_tecnico,id_turno])
        return self.client.post(url)

    # ------------------------ Asignar tecnico ------------------------ #
    def test_tecnico_disponible(self):
        # vamos a asignarle un turno de 10 a 12, papeles en regla --> asigna
        turno = Turno_taller.objects.get(id_turno=4)
        response_esperado ={
                'id_turno': turno.id_turno ,
                'tipo': turno.tipo,
                'estado': 'En proceso',
                'taller_id': turno.taller_id.id_taller,
                'tecnico_id': self.id_tecnico,
                'patente': turno.patente,
                'fecha_inicio': turno.fecha_inicio.strftime("%Y-%m-%d"),
                'hora_inicio': turno.hora_inicio.strftime("%H:%M:%S"),
                'fecha_fin': turno.fecha_fin.strftime("%Y-%m-%d"),
                'hora_fin': turno.hora_fin.strftime("%H:%M:%S"),
                'frecuencia_km': None,
                'papeles_en_regla': True 
            }
        
        self.assertEqual(self.post_response_asignar_tecnico(self.id_tecnico, turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_turno_detalle(turno.id_turno).json(), response_esperado)
        
    def test_tecnico_disponible_2(self):
        # vamos a asignarle un turno de 10 a 13 --> asigna
        turno = Turno_taller.objects.get(id_turno=5)
        response_esperado ={
                'id_turno': turno.id_turno ,
                'tipo': turno.tipo,
                'estado': 'En proceso',
                'taller_id': turno.taller_id.id_taller,
                'tecnico_id': self.id_tecnico,
                'patente': turno.patente,
                'fecha_inicio': turno.fecha_inicio.strftime("%Y-%m-%d"),
                'hora_inicio': turno.hora_inicio.strftime("%H:%M:%S"),
                'fecha_fin': turno.fecha_fin.strftime("%Y-%m-%d"),
                'hora_fin': turno.hora_fin.strftime("%H:%M:%S"),
                'frecuencia_km': None,
                'papeles_en_regla': True 
            }
        
        self.assertEqual(self.post_response_asignar_tecnico(self.id_tecnico, turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_turno_detalle(turno.id_turno).json(), response_esperado)
        
    def test_tecnico_disponible_papeles_no_en_regla(self):
        # vamos a asignarle un turno de 10 a 13 --> no asigna
        turno = Turno_taller.objects.get(id_turno=6)
        self.assertEqual(self.post_response_asignar_tecnico(self.id_tecnico, turno.id_turno).status_code, 400)
        
    def test_tecnico_no_disponible_completo(self): 
        # intentamos asignarle un turno de 13 a 14 --> no asigna
        turno = Turno_taller.objects.get(id_turno=7)
        self.assertEqual(self.post_response_asignar_tecnico(self.id_tecnico, turno.id_turno).status_code, 400)
        
    def test_tecnico_no_disponible_contenido(self):
        # intentamos asignarle un turno de 12 a 15 --> no asigna
        turno = Turno_taller.objects.get(id_turno=8)
        self.assertEqual(self.post_response_asignar_tecnico(self.id_tecnico, turno.id_turno).status_code, 400)
        
    def test_tecnico_no_disponible_final(self):
        # intentamos asignarle un turno de 15 a 17 --> no asigna
        turno = Turno_taller.objects.get(id_turno=9)
        self.assertEqual(self.post_response_asignar_tecnico(self.id_tecnico, turno.id_turno).status_code, 400)

    def test_tecnico_no_disponible_principio(self):
        # intentamos asignarle un turno de 8 a 10 --> no asigna
        turno = Turno_taller.objects.get(id_turno=10)
        self.assertEqual(self.post_response_asignar_tecnico(self.id_tecnico, turno.id_turno).status_code, 400)
