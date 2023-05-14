from faker import Faker
from ddf import G
from rest_framework.test import APITestCase
from rest_framework import status
import pdb
from administracion.models import Turno_taller, Taller

"""
self.taller = G(Taller, id_taller='T001', id_sucursal='S001')
        self.turno_taller = G(Turno_taller, tecnico_id=1, estado='En proceso', taller_id=self.taller)
        self.turno_taller2 = G(Turno_taller, tecnico_id=1, estado='Terminado', taller_id=self.taller)

        self.assertEqual(self.taller, self.turno_taller.taller_id)
        self.assertEqual(Turno_taller.objects.count(), 2)
        self.assertEqual(self.turno_taller.estado, "En proceso")
        self.assertEqual(self.turno_taller2.estado, "Terminado")

        return super().setUp()

    def test_setup(self):
        pass
"""

class TestSetup(APITestCase):
    def setUp(self):
        faker = Faker()
        self.turnos_url = '/turnos/'  
        self.taller = G(Taller, id_taller=1, id_sucursal=1)
        self.turno = G(Turno_taller, tecnico_id=1, tipo= "Evaluacion", estado='En proceso', taller_id=self.taller, fecha_inicio="2023-10-05", fecha_fin="2023-10-05", hora_inicio="10:00:00", hora_fin="12:00:00")
        
        dic = {"id_turno": str(self.turno.id_turno), 
            "tipo": self.turno.tipo,
            "taller_id": str(self.taller.id_taller),
            "patente": self.turno.patente,
            "fecha_inicio": self.turno.fecha_inicio, 
            "hora_inicio": self.turno.hora_inicio, 
            "fecha_fin": self.turno.fecha_fin, 
            "hora_fin": self.turno.hora_fin, 
            "frecuencia_km" : self.turno.frecuencia_km, 
            "papeles_en_regla": self.turno.papeles_en_regla }
        
        response = self.client.post(self.turnos_url + "turnos-create/", dic, format= 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
   
		# para parar la ejecución acá, pdb es un paquete de python que permite detener la ejecución
		# de la funcionalidad que estemos realizando.
		# acá tendríamos nuestro turno creado (?)
        return super().setUp()
    
    def test_sdadas(self):
        pass
