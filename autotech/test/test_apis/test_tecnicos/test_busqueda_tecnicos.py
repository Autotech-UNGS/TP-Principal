from unittest.mock import patch, Mock
from django.urls import reverse
from .test_setup import TestSetUp
from test.factories.tecnicos_factories import UsuarioFactory
from administracion.models import Turno_taller

class BusquedaTecnicoTestCase(TestSetUp):
    # Mock para simular la respuesta de la API externa
    tecnicos =  UsuarioFactory.build_batch(3, tipo="Tecnico", categoria='A')
    tecnicos_mock = [usuario.__dict__ for usuario in tecnicos]

    mock_api_response = Mock()
    mock_api_response.status_code = 200
    mock_api_response.json.return_value = tecnicos_mock


    # -------------------- Test lista_tecnicos -------------------- #

    def get_response_lista_tecnicos(self, id_sucursal):
        with patch('requests.get', return_value=self.mock_api_response):
            url = reverse('lista-tecnicos') + f'?branch={id_sucursal}'
            return self.client.get(url)
        
    def test_obtener_lista_tecnicos_con_sucursal_valida(self):
        sucursal_supervisor = 'S001'
        response_esperado = [
            {
                'id_empleado': tecnico['id_empleado'], 
                'nombre_completo': tecnico['nombre_completo'], 
                'dni': tecnico['dni'], 
                'categoria': tecnico['categoria'], 
                'branch': tecnico['branch']

            } for tecnico in self.tecnicos_mock]
        self.assertEqual(self.get_response_lista_tecnicos(sucursal_supervisor).status_code, 200)
        self.assertDictEqual(self.get_response_lista_tecnicos(sucursal_supervisor).json(), {'tecnicos': response_esperado})

    def test_tecnicos_list_sucursal_sin_tecnicos(self):
        sucursal_sin_tecnicos = 'S002'
        self.assertEqual(self.get_response_lista_tecnicos( sucursal_sin_tecnicos).status_code, 200)
        self.assertDictEqual(self.get_response_lista_tecnicos( sucursal_sin_tecnicos).json(), {'tecnicos': []})

    def test_tecnicos_list_sucursal_invalida1_error_400(self):   
        sucursal_supervisor_invalida1 = 'x001'
        self.assertEqual(self.get_response_lista_tecnicos( sucursal_supervisor_invalida1).status_code, 400)
    
    def  test_tecnicos_list_sucursal_invalida2_error_400(self):   
        sucursal_supervisor_invalida2 = 'S0001'
        self.assertEqual(self.get_response_lista_tecnicos(sucursal_supervisor_invalida2).status_code, 400)

    def test_tecnicos_list_sin_sucursal_error_400(self):
        self.assertEqual(self.get_response_lista_tecnicos('').status_code, 400)

    # -------------------- Test detalle_trabajos_tecnico -------------------- #
      
    def get_response_datalle_trabajos_tecnico(self, id_tecnico, id_sucursal):   
        url = reverse('detalle-trabajos-tecnico', args=[id_tecnico])+ f'?branch={id_sucursal}'
        return self.client.get(url) 
    
    def get_datos_turno(self):
        datos_turnos = list(Turno_taller.objects.all().values(
                "id_turno",
                "patente",
                "fecha_inicio",
                "hora_inicio",
                "fecha_fin",
                "hora_fin",
                "tipo",
                "estado"
        ))
        return datos_turnos
    
    def test_detalle_trabajos_tecnico_ok(self):
       id_primer_tecnico = self.tecnicos_mock[0]['id_empleado']
       sucursal_supervisor = 'S001'
       self.assertEqual(self.get_response_datalle_trabajos_tecnico(id_primer_tecnico, sucursal_supervisor).status_code, 200)
       self.assertEqual(self.get_response_datalle_trabajos_tecnico(id_primer_tecnico, sucursal_supervisor).data, self.get_datos_turno()) 
    
    def test_detalle_trabajos_tecnico_sin_trabajos(self):
       id_tecnico_sin_trabajos = self.tecnicos_mock[2]['id_empleado']
       sucursal_supervisor = 'S001'
       self.assertEqual(self.get_response_datalle_trabajos_tecnico(id_tecnico_sin_trabajos, sucursal_supervisor).status_code, 200)
       self.assertEqual(self.get_response_datalle_trabajos_tecnico(id_tecnico_sin_trabajos, sucursal_supervisor).data, [])

    def test_detalle_trabajos_tecnico_sucursal_de_otro_taller(self):
       id_primer_tecnico = self.tecnicos_mock[0]['id_empleado']
       sucursal_supervisor = 'S002'
       self.assertEqual(self.get_response_datalle_trabajos_tecnico(id_primer_tecnico, sucursal_supervisor).status_code, 200)
       self.assertEqual(self.get_response_datalle_trabajos_tecnico(id_primer_tecnico, sucursal_supervisor).data, [])       
    
    def test_detalle_trabajos_tecnico_sucursal_invalida_error_400(self):
       id_primer_tecnico = self.tecnicos_mock[0]['id_empleado']
       sucursal_supervisor_invalida = 's001'
       self.assertEqual(self.get_response_datalle_trabajos_tecnico(id_primer_tecnico, sucursal_supervisor_invalida).status_code, 400)
    
    # -------------------- Test categorias -------------------- #

    def get_response_categorias(self):   
        url = reverse('categorias')
        return self.client.get(url) 
    
    def test_categorias_validas_ok(self):
        categorias = ['A', 'B', 'C', 'D']
        self.assertEqual(self.get_response_categorias().status_code, 200 )
        self.assertEqual(self.get_response_categorias().json(), categorias)
    
    def test_categorias_no_validas_ok(self):
        categorias = ['T', 'x', 'C', 'D']
        self.assertEqual(self.get_response_categorias().status_code, 200 )
        self.assertNotEqual(self.get_response_categorias().json(), categorias)

    # -------------------- Test filtrar_tecnicos -------------------- #

    def get_response_filtrar_tecnicos(self, id_sucursal, categoria=None, dni=None,  nombre=None):   
        with patch('requests.get', return_value=self.mock_api_response):
            url = reverse('filtrar-tecnicos') + f'?branch={id_sucursal}'
            if categoria is not None:
                url += f'&categoria={categoria}'
            if dni is not None:
                url += f'&dni={dni}'
            if nombre is not None:
                url += f'&nombre_completo={nombre}'
            response = self.client.get(url)    
        return response
    
    def get_response_esperado_filtro(self, tecnico):
        response_esperado = {
                'id_empleado': tecnico['id_empleado'], 
                'nombre_completo': tecnico['nombre_completo'], 
                'dni': tecnico['dni'], 
                'categoria': tecnico['categoria'], 
                'branch': tecnico['branch']
            }
        return response_esperado

    def test_filtrar_tecnicos_todos_los_filtros(self):
        id_sucursal_supervisor = 'S001'
        categoria = self.tecnicos_mock[1]['categoria']
        dni = self.tecnicos_mock[1]['dni']
        nombre = self.tecnicos_mock[1]['nombre_completo']
        
        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=categoria, dni=dni, nombre=nombre).status_code, 200 )   
        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=categoria, dni=dni, nombre=nombre).json(), {'tecnicos':[self.get_response_esperado_filtro(self.tecnicos_mock[1])]})
    
    def test_filtrar_tecnicos_solo_categoria(self):
        id_sucursal_supervisor = 'S001'
        categoria = 'A'
        response_esperado = [
            {
                'id_empleado': tecnico['id_empleado'], 
                'nombre_completo': tecnico['nombre_completo'], 
                'dni': tecnico['dni'], 
                'categoria': tecnico['categoria'], 
                'branch': tecnico['branch']

            } for tecnico in self.tecnicos_mock]
        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=categoria, dni=None, nombre=None).status_code, 200 )   
        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=categoria, dni=None, nombre=None).json(), {'tecnicos':response_esperado})    
    
    def test_filtrar_tecnicos_solo_dni(self):
        id_sucursal_supervisor = 'S001'
        dni = self.tecnicos_mock[0]['dni']

        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=None, dni=dni, nombre=None).status_code, 200 )   
        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=None, dni=dni, nombre=None).json(), {'tecnicos':[self.get_response_esperado_filtro(self.tecnicos_mock[0])]})    
    
    def test_filtrar_tecnicos_sucursal_invalida_error_400(self):
        id_sucursal_supervisor = '9901'
        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=None, dni=None, nombre=None).status_code, 400)   
    
    def test_filtrar_tecnicos_categoria_invalida_error_400(self):
        id_sucursal_supervisor = 'S001'
        categoria= '2'
        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=categoria, dni=None, nombre=None).status_code, 400 )   
    
    def test_filtrar_tecnicos_dni_invalido_error_400(self):
        id_sucursal_supervisor = 'S001'
        dni = '-0'
        self.assertEqual(self.get_response_filtrar_tecnicos(id_sucursal=id_sucursal_supervisor, categoria=None, dni=dni, nombre=None).status_code, 400 )   