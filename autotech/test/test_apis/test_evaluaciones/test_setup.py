from ddf import G
from rest_framework.test import APITestCase
from administracion.models import Turno_taller, Taller, Registro_evaluacion, Checklist_evaluacion

class TestSetUp(APITestCase):

    def setUp(self):
        self.tarea_evaluacion1 = G(Checklist_evaluacion,  elemento='Cuadro de instrumentos', tarea='Comprobar funcionamiento', costo_reemplazo=30000.0, duracion_reemplazo=480, puntaje_max=50)
        self.tarea_evaluacion2 = G(Checklist_evaluacion,elemento='Faros', tarea='Comprobar funcionamiento', costo_reemplazo=15518.0, duracion_reemplazo=60, puntaje_max=15)
        self.tarea_evaluacion3 = G(Checklist_evaluacion, elemento='Luces de emergencia', tarea='Comprobar funcionamiento', costo_reemplazo=5199.0, duracion_reemplazo=30, puntaje_max=15)
        self.tarea_evaluacion4 = G(Checklist_evaluacion, elemento='Luces Intermitentes', tarea='Comprobar funcionamiento', costo_reemplazo=17109.0, duracion_reemplazo=30, puntaje_max=15)


        # Instancias modelos
        self.taller = G(Taller, id_taller=1, estado=True) 

        # Para testear que el registro que se guarde en registro_evaluacion sea de un turno tipo 'evaluacion'     
        self.turno_taller1 = G(Turno_taller, tipo='evaluacion', tecnico_id=1, estado='en_proceso', taller_id=self.taller, papeles_en_regla=True ) # id=1
        self.turno_taller2 = G(Turno_taller, tipo='service', tecnico_id=1, estado='en_proceso', taller_id=self.taller) # id=2
        self.turno_taller3 = G(Turno_taller, tipo='reparacion', tecnico_id=1, estado='en_proceso', taller_id=self.taller) # id=3
        self.turno_taller4 = G(Turno_taller, tipo='extraordinario', tecnico_id=1, estado='en_proceso', taller_id=self.taller) # id=4

        # Para testear que el registro que se guarde en registro_evaluacion sea de un turno con estado 'en_proceso'    
        self.turno_taller5 = G(Turno_taller, tipo='evaluacion', tecnico_id=1, estado='en_proceso', taller_id=self.taller,papeles_en_regla=True) # id=5
        self.turno_taller6 = G(Turno_taller, tipo='evaluacion', tecnico_id=None, estado='pendiente', taller_id=self.taller,papeles_en_regla=True) # id=6
        self.turno_taller7 = G(Turno_taller, tipo='evaluacion', tecnico_id=1, estado='terminado', taller_id=self.taller,papeles_en_regla=True) # id=7
        self.turno_taller8 = G(Turno_taller, tipo='evaluacion', tecnico_id=None, estado='cancelado', taller_id=self.taller,papeles_en_regla=True) # id=8

        self.turno_taller9 = G(Turno_taller, tipo='evaluacion', tecnico_id=1, estado='en_proceso', taller_id=self.taller,papeles_en_regla=True) # id=9 -> turno ya registrado en el registro_evaluacion      
        self.id_task_puntaje_data = {
                                        "1": 0,
                                        "2": 0,
                                        "3": 0,
                                        "4": 10
                                     }
        self.evaluacion_registrada = G(Registro_evaluacion, id_turno=self.turno_taller9, id_task_puntaje=self.id_task_puntaje_data, detalle='hola' ) 

        self.assertEqual(Checklist_evaluacion.objects.count(), 4) # solo creamos cuatro tareas en la checklist para probar

        self.assertEqual(self.taller, self.turno_taller1.taller_id)

        self.assertEqual(Turno_taller.objects.count(), 9)

        self.assertEqual(Turno_taller.objects.filter(estado='en_proceso').count(), 6)
        self.assertEqual(Turno_taller.objects.filter(estado='pendiente').count(), 1)
        self.assertEqual(Turno_taller.objects.filter(estado='terminado').count(), 1)
        self.assertEqual(Turno_taller.objects.filter(estado='cancelado').count(), 1)

        self.assertEqual(Turno_taller.objects.filter(tipo='evaluacion').count(), 6)
        self.assertEqual(Turno_taller.objects.filter(tipo='service').count(), 1)
        self.assertEqual(Turno_taller.objects.filter(tipo='reparacion').count(), 1)
        self.assertEqual(Turno_taller.objects.filter(tipo='extraordinario').count(), 1)

        self.assertEqual(Registro_evaluacion.objects.count(), 1)

        return super().setUp()
    
    def test_setup(self):
        pass  