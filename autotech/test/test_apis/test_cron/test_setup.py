from ddf import G
from rest_framework.test import APITestCase
from administracion.models import Turno_taller, Taller
from datetime import date, timedelta

class TestSetUp(APITestCase):
    def setUp(self):
        # Instancias modelos
        self.taller = G(Taller, id_taller=1, estado=True)
        ayer = date.today() - timedelta(days=1)
        hoy = date.today() # --> empieza hoy
        mañana = date.today() + timedelta(days=1)
        
        # turnos que debian empezar hoy y no lo hicieron:
        self.turno_ausente = G(Turno_taller, id_turno=200, tipo='service', fecha_inicio = hoy, fecha_fin= hoy , tecnico_id=None, estado='pendiente', taller_id=self.taller,papeles_en_regla=True )
        self.turno_ausente = G(Turno_taller, id_turno=201, tipo='service', fecha_inicio = hoy, fecha_fin= mañana, tecnico_id=None, estado='pendiente', taller_id=self.taller,papeles_en_regla=True )
        
        # turnos que debian terminar hoy y no lo hicieron:
        self.turno_ausente = G(Turno_taller, id_turno=300, tipo='service', fecha_inicio = hoy, fecha_fin= hoy , tecnico_id=None, estado='en_proceso', taller_id=self.taller,papeles_en_regla=True )
        self.turno_ausente = G(Turno_taller, id_turno=301, tipo='service', fecha_inicio = ayer, fecha_fin= hoy , tecnico_id=None, estado='en_proceso', taller_id=self.taller,papeles_en_regla=True )
        
        # turnos que no deben cambiar --> empezaron/terminaron correctamente hoy
        # empezo y termino hoy: --> ya esta terminado
        self.turno_ausente = G(Turno_taller, id_turno=400, tipo='service', fecha_inicio = hoy, fecha_fin= hoy , tecnico_id=None, estado='terminado', taller_id=self.taller,papeles_en_regla=True )
        # empezo hoy, fue asignado, y termina mañana --> ya esta empezado
        self.turno_ausente = G(Turno_taller, id_turno=401, tipo='service', fecha_inicio = hoy, fecha_fin= mañana , tecnico_id=None, estado='en_proceso', taller_id=self.taller,papeles_en_regla=True )
        
        return super().setUp()
    
    def test_setup(self):
        pass
