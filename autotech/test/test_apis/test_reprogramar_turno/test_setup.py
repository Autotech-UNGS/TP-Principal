from faker import Faker
from ddf import G
from rest_framework.test import APITestCase
from rest_framework import status
import pdb
from administracion.models import Turno_taller
from administracion.models import Taller
from datetime import date, time
import json

class TestSetUp(APITestCase):
    def setUp(self):
        self.taller1 = G(Taller, id_taller=10, capacidad=10)
        
        # evaluacion --> 2023/06/29, 10-11hs
        self.turno_evaluacion_valido1 = G(Turno_taller, id_turno=100, tipo='evaluacion', estado='cancelado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=True)
        self.turno_evaluacion_valido2 = G(Turno_taller, id_turno=101, tipo='evaluacion', estado='cancelado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        
        self.turno_evaluacion_invalido1 = G(Turno_taller, id_turno=102, tipo='evaluacion', estado='pendiente', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        self.turno_evaluacion_invalido2 = G(Turno_taller, id_turno=103, tipo='evaluacion', estado='rechazado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        self.turno_evaluacion_invalido3 = G(Turno_taller, id_turno=104, tipo='evaluacion', estado='terminado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        self.turno_evaluacion_invalido4 = G(Turno_taller, id_turno=105, tipo='evaluacion', estado='ausente', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        self.turno_evaluacion_invalido5 = G(Turno_taller, id_turno=106, tipo='evaluacion', estado='en_proceso', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(10,0,0), fecha_fin=date(2023,6,29), hora_fin=time(11,0,0),frecuencia_km=None, papeles_en_regla=False)
        
        # service --> 2023/06/29, 13-15hs
        self.turno_service_valido1 = G(Turno_taller, id_turno=200, tipo='service', estado='cancelado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,29), hora_fin=time(15,0,0),frecuencia_km=5000, papeles_en_regla=True)
        
        self.turno_service_invalido1 = G(Turno_taller, id_turno=201, tipo='service', estado='pendiente', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,29), hora_fin=time(15,0,0),frecuencia_km=5000, papeles_en_regla=True)
        self.turno_service_invalido2 = G(Turno_taller, id_turno=202, tipo='service', estado='rechazado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,29), hora_fin=time(15,0,0),frecuencia_km=5000, papeles_en_regla=True)
        self.turno_service_invalido3 = G(Turno_taller, id_turno=203, tipo='service', estado='terminado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,29), hora_fin=time(15,0,0),frecuencia_km=5000, papeles_en_regla=True)
        self.turno_service_invalido4 = G(Turno_taller, id_turno=204, tipo='service', estado='ausente', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,29), hora_fin=time(15,0,0),frecuencia_km=5000, papeles_en_regla=True)
        self.turno_service_invalido5 = G(Turno_taller, id_turno=205, tipo='service', estado='en_proceso', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,29), hora_fin=time(15,0,0),frecuencia_km=5000, papeles_en_regla=True)
        
        # reparaciones --> 2023/06/29, 15-17hs --> vamos a intentar reprogramarlo a una hora que no se pueda (2023/06/30 a las 8, o el 2029/06/29 a las 16).
        self.turno_reparacion_valido1 = G(Turno_taller, id_turno=300, tipo='reparacion', estado='cancelado', taller_id=10, tecnico_id=None, patente='ABC123', fecha_inicio=date(2023,6,29), hora_inicio=time(13,0,0), fecha_fin=date(2023,6,29), hora_fin=time(15,0,0),frecuencia_km=5000, papeles_en_regla=True)
        
        # saturamos --> 2023/06/30, 8hs
        self.turno_relleno1 = G(Turno_taller, id_turno= 107, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno2 = G(Turno_taller, id_turno= 108, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno3 = G(Turno_taller, id_turno= 109, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno4 = G(Turno_taller, id_turno= 110, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno5 = G(Turno_taller, id_turno= 111, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno6 = G(Turno_taller, id_turno= 112, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno7 = G(Turno_taller, id_turno= 113, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno8 = G(Turno_taller, id_turno= 114, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno9 = G(Turno_taller, id_turno= 115, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))
        self.turno_relleno10 = G(Turno_taller, id_turno= 116, tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,6,30), hora_inicio=time(8,0,0), fecha_fin=date(2023,6,30), hora_fin=time(9,0,0))

        
        self.turno_relleno10 = G(Turno_taller, id_turno= 117, patente="FRN198", tipo='evaluacion', estado='cancelado', taller_id=10, fecha_inicio=date(2023,10,15), hora_inicio=time(8,0,0), fecha_fin=date(2023,10,15), hora_fin=time(9,0,0))
        # el turno 117 no puede reagendarse para el 2023/10/16 a ninguna hora, porque ya tiene un turno de evaluacion para ese dia
        self.turno_relleno10 = G(Turno_taller, id_turno= 118, patente="FRN198", tipo='evaluacion', estado='pendiente', taller_id=10, fecha_inicio=date(2023,10,16), hora_inicio=time(8,0,0), fecha_fin=date(2023,10,16), hora_fin=time(9,0,0))
        # tampoco puede reagendarse para el 2023/10/17 a las 8, porque tiene un turno para otra cosa ese dia --> pero sí puede reagendarlo a otro horario
        self.turno_relleno10 = G(Turno_taller, id_turno= 119, patente="FRN198", tipo='service', frecuencia_km=5000, estado='pendiente', taller_id=10, fecha_inicio=date(2023,10,17), hora_inicio=time(8,0,0), fecha_fin=date(2023,10,17), hora_fin=time(9,0,0))

        return super().setUp()
    
    def test_setup(self):
        pass