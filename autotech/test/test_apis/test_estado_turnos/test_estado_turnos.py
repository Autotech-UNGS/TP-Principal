from unittest.mock import patch, Mock
from django.urls import reverse
from .test_setup import TestSetUp
from test.factories.usuario_factorie import UsuarioFactory
from administracion.models import Turno_taller

class EstadoTurnosUsuarioFactory(UsuarioFactory):
    pass

class EstadoTurnosTestCase(TestSetUp):

    #Mock para simular la respuesta de la API externa
    tecnicos = [
        UsuarioFactory.build(id_empleado=1, tipo="Tecnico", categoria='A'),
        UsuarioFactory.build(id_empleado=2, tipo="Tecnico", categoria='B'),
        UsuarioFactory.build(id_empleado=3, tipo="Tecnico", categoria='D')
    ]  # tecnico 1 es el unico con turnos trabajados
    tecnicos_mock = [usuario.__dict__ for usuario in tecnicos]

    mock_api_response = Mock()
    mock_api_response.status_code = 200
    mock_api_response.json.return_value = tecnicos_mock
    # -------------------- Test turnos_pendientes -------------------- #
    def get_response_turnos_pendientes(self, sucursal_supervisor, papeles_en_regla):
        url = reverse('turnos-pendientes') + f'?'
        if sucursal_supervisor is not None:
                url += f'branch={sucursal_supervisor}&'
        if papeles_en_regla is not None:
                url += f'papeles_en_regla={papeles_en_regla}'
        return self.client.get(url)
    
    def get_response_turnos_pendientes_esperado(self, sucursal_supervisor, papeles_en_regla):
        id_sucursal = int(sucursal_supervisor[-3:])
        turnos_pendientes = Turno_taller.objects.filter(estado='pendiente', taller_id=id_sucursal, papeles_en_regla=papeles_en_regla)
        turnos_data = []
        for turno in turnos_pendientes:
            turno_data = {
                'id_turno': turno.id_turno,
                'patente': turno.patente,
                'estado': turno.estado,
                'tipo': turno.tipo,
                'fecha_inicio': turno.fecha_inicio,
                'hora_inicio': turno.hora_inicio,
            }
            turnos_data.append(turno_data)
        return turnos_data


    def test_cant_pendientes_de_aprobacion(self):
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='false').status_code, 200)
        self.assertEqual(len(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='false').data), 1)

    def test_cant_pendientes_aprobados(self):
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='true').status_code, 200)
        self.assertEqual(len(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='true').data), 4)
    
    def test_pendientes_sin_info_papeles_error_400(self):
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla=None).status_code, 400)
    
    def test_pendientes_info_papeles_invalida_error_400(self):
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='aprobado').status_code, 400)
    
    def test_pendientes_sin_sucursal_error_400(self):
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor=None, papeles_en_regla='false').status_code, 400)
    
    def test_pendientes_sucursal_invalida_error_400(self):
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='tv01', papeles_en_regla='true').status_code, 400)
    
    def test_pendientes_de_aprobacion_comparar_data_esperada(self):
        response_esperado = self.get_response_turnos_pendientes_esperado(sucursal_supervisor='S001', papeles_en_regla=False)
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='false').status_code, 200)
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='false').data, response_esperado)
    
    """ def test_pendientes_aprobados_comparar_data_esperada(self):
        response_esperado = self.get_response_turnos_pendientes_esperado(sucursal_supervisor='S001', papeles_en_regla=True)
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='true').status_code, 200)
        self.assertEqual(self.get_response_turnos_pendientes(sucursal_supervisor='S001', papeles_en_regla='true').data, response_esperado) """
    
    # -------------------- Test turnos_en_proceso -------------------- #
    # solo existe un tecnico trabajando en sucursal 1, asi que parcheamos el metodo para que devuelve
    # unicamente el nombre del tecnico 1
    def get_response_turnos_en_proceso(self, sucursal_supervisor):
        with patch('turnos.detalle_turnos_views.ConsumidorApiTecnicos.obtener_nombre_tecnico', return_value=self.tecnicos_mock[0]['nombre_completo'] ):
            url = reverse('turnos-en-procesos') + f'?'
            if sucursal_supervisor is not None:
                url += f'branch={sucursal_supervisor}'
            #import pdb; pdb.set_trace()
            return self.client.get(url)
    
    def get_response_turnos_en_proceso_esperado(self, sucursal_supervisor):
        id_sucursal = int(sucursal_supervisor[-3:])
        turnos_en_proceso = Turno_taller.objects.filter(estado='en_proceso', taller_id=id_sucursal)
        turnos_data = []
        for turno in turnos_en_proceso:
            turno_data = {
                'id_turno': turno.id_turno,
                'patente': turno.patente,
                'estado': 'en proceso',
                'tipo': turno.tipo,
                'fecha_inicio': turno.fecha_inicio,
                'hora_inicio': turno.hora_inicio,
                'tecnico_id': turno.tecnico_id,
                'nombre_completo': self.tecnicos_mock[0]['nombre_completo'] 
            }
            turnos_data.append(turno_data)
        return turnos_data       

    def test_cant_en_proceso(self):   
        self.assertEqual(self.get_response_turnos_en_proceso(sucursal_supervisor='S001').status_code, 200)
        self.assertEqual(len(self.get_response_turnos_en_proceso(sucursal_supervisor='S001').data), 4)
        
    def test_en_proceso_comparar_data_esperada(self):
        response_esperado = self.get_response_turnos_en_proceso_esperado(sucursal_supervisor='S001')
        self.assertEqual(self.get_response_turnos_en_proceso(sucursal_supervisor='S001').status_code, 200)
        self.assertEqual(self.get_response_turnos_en_proceso(sucursal_supervisor='S001').data, response_esperado)
    
    def test_en_proceso_sucursal_invalida_error_400(self): 
        self.assertEqual(self.get_response_turnos_en_proceso(sucursal_supervisor='s9c9').status_code, 400)
    
    def test_pendientes_sin_sucursal_error_400(self):
        self.assertEqual(self.get_response_turnos_en_proceso(sucursal_supervisor=None).status_code, 400)
    # -------------------- Test turnos_terminados -------------------- #
    def get_response_turnos_terminados(self, sucursal_supervisor):
        with patch('turnos.detalle_turnos_views.ConsumidorApiTecnicos.obtener_nombre_tecnico', return_value=self.tecnicos_mock[0]['nombre_completo'] ):
            url = reverse('turnos-terminados') + f'?'
            if sucursal_supervisor is not None:
                url += f'branch={sucursal_supervisor}'
            return self.client.get(url)
    
    def get_response_turnos_terminados_esperado(self, sucursal_supervisor):
        id_sucursal = int(sucursal_supervisor[-3:])
        turnos_en_proceso = Turno_taller.objects.filter(estado='terminado', taller_id=id_sucursal)
        turnos_data = []
        for turno in turnos_en_proceso:
            turno_data = {
                    'id_turno': turno.id_turno,
                    'patente': turno.patente,
                    'estado': turno.estado,
                    'tipo': turno.tipo,
                    'fecha_inicio': turno.fecha_inicio,
                    'hora_inicio': turno.hora_inicio,
                    'fecha_fin': turno.fecha_fin,
                    'hora_fin': turno.hora_fin,
                    'tecnico_id': turno.tecnico_id,
                    'nombre_completo': self.tecnicos_mock[0]['nombre_completo'],          
            }
            turnos_data.append(turno_data)
        return turnos_data
    
    def test_cant_terminados(self):
        self.assertEqual(self.get_response_turnos_terminados(sucursal_supervisor='S001').status_code, 200)
        self.assertEqual(len(self.get_response_turnos_terminados(sucursal_supervisor='S001').data), 1)

    def test_terminados_comparar_data_esperada(self):
        response_esperado = self.get_response_turnos_terminados_esperado(sucursal_supervisor='S001')
        self.assertEqual(self.get_response_turnos_terminados(sucursal_supervisor='S001').status_code, 200)
        self.assertEqual(self.get_response_turnos_terminados(sucursal_supervisor='S001').data, response_esperado)
    
    def test_terminados_sucursal_invalida_error_400(self): 
        self.assertEqual(self.get_response_turnos_terminados(sucursal_supervisor='c890').status_code, 400)

    def test_pendientes_sin_sucursal_error_400(self):
        self.assertEqual(self.get_response_turnos_terminados(sucursal_supervisor=None).status_code, 400) 

    # -------------------- Test actualizar_estado_turno_en_proceso -------------------- #
    def get_response_actualizar_estado_turno_en_proceso(self, id_turno):
        url = reverse('actualizar-estado-turno', args=[id_turno])
        return self.client.patch(url)

    def test_actualizar_en_proceso_a_terminado_ok(self):
        turno_cancelar = Turno_taller.objects.all()[5] 
        response = self.get_response_actualizar_estado_turno_en_proceso(id_turno=turno_cancelar.id_turno)
        self.assertEqual(turno_cancelar.estado, 'en_proceso')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Turno_taller.objects.all()[5] .estado, 'terminado')
    
    
    def test_actualizar_pendiente_a_terminado_error_400(self):
        turno_cancelar = Turno_taller.objects.all()[1] 
        response = self.get_response_actualizar_estado_turno_en_proceso(id_turno=turno_cancelar.id_turno)
        self.assertEqual(turno_cancelar.estado, 'pendiente')
        self.assertEqual(response.status_code, 400)
    

    def test_actualizar_terminado_a_terminado_error_400(self):
        turno_cancelar = Turno_taller.objects.all()[9] 
        response = self.get_response_actualizar_estado_turno_en_proceso(id_turno=turno_cancelar.id_turno)
        self.assertEqual(turno_cancelar.estado, 'terminado')
        self.assertEqual(response.status_code, 400)
    
    def test_actualizar_cancelado_a_terminado_error_400(self):
        turno_cancelar = Turno_taller.objects.all()[10] 
        response = self.get_response_actualizar_estado_turno_en_proceso(id_turno=turno_cancelar.id_turno)
        self.assertEqual(turno_cancelar.estado, 'cancelado')
        self.assertEqual(response.status_code, 400)
    

    # -------------------- Test cancelar_turno_pendiente -------------------- #
    def get_response_cancelar_turno_pendiente(self, id_turno):
        url = reverse('cancelar-turno-pendiente', args=[id_turno])
        return self.client.patch(url)

    def test_cancelar_turno_pendiente_ok(self):
        turno_cancelar = Turno_taller.objects.all()[0] 
        response = self.get_response_cancelar_turno_pendiente(id_turno=turno_cancelar.id_turno)
        self.assertEqual(turno_cancelar.estado, 'pendiente')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Turno_taller.objects.all()[0].estado, 'cancelado')
    
    def test_cancelar_turno_en_proceso_error_40(self):
        turno_cancelar = Turno_taller.objects.all()[5] 
        response = self.get_response_cancelar_turno_pendiente(id_turno=turno_cancelar.id_turno)
        self.assertEqual(turno_cancelar.estado, 'en_proceso')
        self.assertEqual(response.status_code, 400)
    
    def test_cancelar_turno_terminado_error_400(self):
        turno_cancelar = Turno_taller.objects.all()[9] 
        response = self.get_response_cancelar_turno_pendiente(id_turno=turno_cancelar.id_turno)
        self.assertEqual(turno_cancelar.estado, 'terminado')
        self.assertEqual(response.status_code, 400)
    
    def tes_cancelar_turno_cancelado_error_400(self):
        turno_cancelar = Turno_taller.objects.all()[10] 
        response = self.get_response_cancelar_turno_pendiente(id_turno=turno_cancelar.id_turno)
        self.assertEqual(turno_cancelar.estado, 'cancelado')
        self.assertEqual(response.status_code, 400)
    
