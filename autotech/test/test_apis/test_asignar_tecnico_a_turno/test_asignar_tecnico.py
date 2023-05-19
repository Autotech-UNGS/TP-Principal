from unittest.mock import patch, Mock
from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.views import *
from test.factories.usuario_factorie import *

class AsignarTecnicoTestCase(TestSetUp):
    id_tecnico = 2
    tecnico =  UsuarioFactory.build(id_empleado=2, tipo="Tecnico", categoria='A', branch='T001')

    def get_response_turno_detalle(self, id_turno):
        url = reverse('turnos-detalle', args=[id_turno])
        return self.client.get(url)
        
    def post_response_asignar_tecnico(self, id_tecnico, id_turno):
        url = reverse('asignar-tecnico', args=[id_tecnico, id_turno])
        return self.client.post(url)

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
            'frecuencia_km': turno.frecuencia_km,
            'papeles_en_regla': True 
            }
        return response_esperado
        
    # ------------------------ Asignar tecnico ------------------------ #
    # Taller 1 --> tecnico 2. Como el turno 11 no existe en la bbdd, no hay problema
    def test_tecnico_disponible(self):
        turno = Turno_taller.objects.get(id_turno=11)
        response_esperado = self.generar_response_esperado_asignar_tecnico(turno)
        
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_turno_detalle(turno.id_turno).json(), response_esperado)
        
    # Taller 1 --> tecnico 2. Como el turno 12 no existe en la bbdd, no hay problema        
    def test_tecnico_disponible_2(self):
        turno = Turno_taller.objects.get(id_turno=12)
        response_esperado = self.generar_response_esperado_asignar_tecnico(turno)
        
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 200)
        self.assertDictEqual(self.get_response_turno_detalle(turno.id_turno).json(), response_esperado)
        
    def test_turno_ya_asignado(self):
        turno = Turno_taller.objects.get(id_turno=13)
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 400)        
        
    def test_tecnico_disponible_papeles_no_en_regla(self):
        turno = Turno_taller.objects.get(id_turno=14)
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 400)
        
    # le asignamos un turno a la misma hora, asi que no esta disponible
    def test_tecnico_no_disponible_completo(self): 
        turno = Turno_taller.objects.get(id_turno=17)
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 400)
        
    def test_tecnico_no_disponible_contenido(self):
        turno = Turno_taller.objects.get(id_turno=16)
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 400)
        
    def test_tecnico_no_disponible_final(self):
        turno = Turno_taller.objects.get(id_turno=18)
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 400)

    def test_tecnico_no_disponible_principio(self):
        turno = Turno_taller.objects.get(id_turno=19)
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 400)

    # el tecnico pertenece al taller 2, y ese turno pertenece al taller 3
    def test_tecnico_pertenece_a_otro_taller(self):
        turno = Turno_taller.objects.get(id_turno=20)
        self.assertEqual(self.post_response_asignar_tecnico(2, turno.id_turno).status_code, 400)