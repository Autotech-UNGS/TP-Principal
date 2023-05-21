import json
from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Registro_evaluacion_para_admin, Registro_evaluacion, Checklist_evaluacion, Turno_taller
from administracion.serializers import ChecklistEvaluacionSerializer, RegistroEvaluacionSerializer,  RegistroEvaluacionXAdminSerializerGET

class RegistroEvaluacionCreateTestCase(TestSetUp):

    def get_response_crear_registro_evaluacion(self, evaluacion_data):
        url = reverse('crear_registro_evaluacion')
        evaluacion_data_json = json.dumps(evaluacion_data)  # Convertir a JSON
        return self.client.post(url, data=evaluacion_data_json, content_type='application/json')
    
    # len(tasks) == len(filas_checklist)
    def get_evaluacion_a_registrar(self, id_turno, id_task, puntaje):
        evaluacion_data =  {
                    "id_turno": id_turno,
                    "id_task_puntaje": {
                        id_task: puntaje,
                        "2": 0,
                        "3": 0,
                        "4": 0,
                    },
                    "detalle": ""
                }
        return evaluacion_data
    
    # len(tasks) < len(filas_checklist)
    def get_evaluacion_a_registrar_menos_tasks_que_checklist(self):
        evaluacion_data =  {
                    "id_turno": 1,
                    "id_task_puntaje": {
                        "1": 0,
                        "2": 0,
                        "3": 0,
                    },
                    "detalle": ""
                }
        return evaluacion_data
    
    # len(tasks) > len(filas_checklist)
    def get_evaluacion_a_registrar_mas_tasks_que_checklist(self):
        evaluacion_data =  {
                    "id_turno": 1,
                    "id_task_puntaje": {
                        "1": 0,
                        "2": 0,
                        "3": 0,
                        "4": 0,
                        "5": 0,
                    },
                    "detalle": ""
                }
        return evaluacion_data

    def test_task_len_menor_a_checklist_evalucion_error_400(self):
        self.assertEqual(self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar_menos_tasks_que_checklist()).status_code, 400)

    def test_task_len_superior_a_checklist_evalucion_error_400(self):
        self.assertEqual(self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar_mas_tasks_que_checklist()).status_code, 400)

    def test_registrar_evaluacion_ok(self):
        id_turno=1
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=id_turno, id_task='1', puntaje=10))
        #import pdb; pdb.set_trace()
        self.assertEqual(registrar_evaluacion.status_code, 201)
        self.assertEqual(registrar_evaluacion.data['id_turno'], id_turno)
  
    def test_id_task_no_existe_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=1,id_task='62',puntaje=None))
        self.assertEqual(registrar_evaluacion.status_code, 400)
    
    def test_puntaje_none_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=1,id_task='1',puntaje=None))
        self.assertEqual(registrar_evaluacion.status_code, 400)

    def test_puntaje_negativo_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=1,id_task='1',puntaje=-1))
        self.assertEqual(registrar_evaluacion.status_code, 400)
    
    def test_puntaje_superior_al_limite_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=1,id_task='1',puntaje=51))
        self.assertEqual(registrar_evaluacion.status_code, 400)
    
    def test_id_turno_tipo_service_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=2,id_task='1',puntaje=40))
        self.assertEqual(registrar_evaluacion.status_code, 400)

    def test_id_turno_tipo_reparacion_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=3,id_task='1',puntaje=40))
        self.assertEqual(registrar_evaluacion.status_code, 400)

    def test_id_turno_tipo_extraordinario_error_400(self): 
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=4,id_task='1',puntaje=40))
        self.assertEqual(registrar_evaluacion.status_code, 400)   
    
    def test_id_turno_estado_pendiente_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=6,id_task='1',puntaje=40))
        self.assertEqual(registrar_evaluacion.status_code, 400) 
    
    def test_id_turno_estado_terminado_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=7,id_task='1',puntaje=40))
        self.assertEqual(registrar_evaluacion.status_code, 400)   

    def test_id_turno_estado_cancelado_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=8,id_task='1',puntaje=40))
        self.assertEqual(registrar_evaluacion.status_code, 400) 
    
    def test_id_turno_en_registro_evaluacion_error_400(self):
        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=9, id_task='1', puntaje=40))
        self.assertEqual(registrar_evaluacion.status_code, 400)     

    def test_creacion_registro_para_admin_ok(self):
        id_turno = 1
        costo_total = 30000.0
        duracion_total_reparaciones = 480

        registrar_evaluacion = self.get_response_crear_registro_evaluacion(self.get_evaluacion_a_registrar(id_turno=id_turno, id_task='1', puntaje=40)) # el happy path
        registro_evaluacion_admin = Registro_evaluacion_para_admin.objects.get(id_turno=id_turno)

        self.assertEqual(registrar_evaluacion.status_code, 201)
        self.assertEqual(registro_evaluacion_admin.id_turno, Turno_taller.objects.get(id_turno=id_turno)) # verificamos que efectivamente se haya creado el registro en la tabla registro_evaluacion_para_admin
        self.assertEqual(registro_evaluacion_admin.costo_total, costo_total)
        self.assertEqual(registro_evaluacion_admin.duracion_total_reparaciones, duracion_total_reparaciones)


class RegistroEvaluacionListTestCase(TestSetUp):
    def get_response_registro_evaluacion_list(self):
        url = reverse('listar_registro_evaluacion')
        return self.client.get(url)

    def test_cant_registro_evaluacion_ok(self):
        self.assertEqual(self.get_response_registro_evaluacion_list().status_code, 200)
        self.assertEqual(len(self.get_response_registro_evaluacion_list().data), 1) # en el setUp solo creamos 1

    def test_listar_registro_evaluacion(self):
        registros = Registro_evaluacion.objects.all()
        serializer = RegistroEvaluacionSerializer(registros, many=True)
        self.assertEqual(self.get_response_registro_evaluacion_list().status_code, 200)
        self.assertEqual(len(self.get_response_registro_evaluacion_list().data), 1)

class RegistroEvaluacionUnoTestCase(TestSetUp):  
    def get_response_registro_evaluacion_uno(self, id_turno):
        url = reverse('listar_registros_evaluacion_por_id', args=[id_turno])
        return self.client.get(url)

    def test_registro_evaluaciones_no_existe_error_404(self):
        id_turno = 10 # no existe registro evaluacion con este id de turno
        self.assertEqual(self.get_response_registro_evaluacion_uno(id_turno=id_turno).status_code, 404)
      
    def test_registro_evaluacion_ok(self):
        id_turno = 9 # existe registro evaluacion con el id de turno
        registros = Registro_evaluacion.objects.filter(id_turno=id_turno)
        serializer = RegistroEvaluacionSerializer(registros, many=True)
        self.assertEqual(self.get_response_registro_evaluacion_uno(id_turno=id_turno).status_code, 200)
        self.assertEqual(self.get_response_registro_evaluacion_uno(id_turno=id_turno).data, serializer.data)


class RegistroEvaluacionXAdminReadOnlyTestCase(TestSetUp):   
    def get_response_registro_evaluacion_x_admin_read_only(self):
        url = reverse('listar_registro_evaluacion_admin')
        return self.client.get(url)
    
    def test_cant_registro_evaluacion_para_admin_ok(self):
        self.assertEqual(self.get_response_registro_evaluacion_x_admin_read_only().status_code, 200)
        self.assertEqual(len(self.get_response_registro_evaluacion_x_admin_read_only().data), 1) # solo debe haber 1 creado

    def test_listar_registro_evaluacion_para_admin(self):
        registros = Registro_evaluacion_para_admin.objects.all()
        serializer = RegistroEvaluacionXAdminSerializerGET(registros, many=True)
        self.assertEqual(self.get_response_registro_evaluacion_x_admin_read_only().status_code, 200)
        self.assertEqual(self.get_response_registro_evaluacion_x_admin_read_only().data, serializer.data) 

class ChecklistEvaluacionListTestCase(TestSetUp):   
    def get_response_checklist_evaluacion_list(self):
        url = reverse('listar_checklist_evaluacion')
        return self.client.get(url)
    
    def test_cant_checklist_evaluacion_ok(self):
        self.assertEqual(self.get_response_checklist_evaluacion_list().status_code, 200)
        self.assertEqual(len(self.get_response_checklist_evaluacion_list().data), 4) # en el setUp solo creamos 4

    def test_listar_checklist_evaluacion(self):
        checklist = Checklist_evaluacion.objects.all()
        serializer = ChecklistEvaluacionSerializer(checklist, many=True)
        self.assertEqual(self.get_response_checklist_evaluacion_list().status_code, 200)
        self.assertEqual(self.get_response_checklist_evaluacion_list().data, serializer.data)