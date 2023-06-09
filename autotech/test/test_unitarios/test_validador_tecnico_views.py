""" import unittest
from tecnicos.validadores_views import ValidadorDatosTecnico, ValidadorDatosSupervisor

class TestValidadorDatosTecnico(unittest.TestCase):
    validador_tec = ValidadorDatosTecnico()

    # ------------------ validacion de categoria tecnico ------------------ #
    def test_categoria_valida(self):
        categoria = 'D'
        self.assertTrue(self.validador_tec.categoria(categoria))  
    
    def test_categoria_none(self):
        categoria = None
        self.assertTrue(self.validador_tec.categoria(categoria)) 

    def test_categoria_numero(self):
        categoria = 2
        self.assertFalse(self.validador_tec.categoria(categoria))

    def test_categoria_minuscula(self):
        categoria = 'a'
        self.assertFalse(self.validador_tec.categoria(categoria))

    def test_categoria_inexistente(self):
        categoria = 'T'
        self.assertFalse(self.validador_tec.categoria(categoria))   

    # ------------------ validacion dni de un tecnico ------------------ #
    def test_dni_valido(self):
        dni = '34565301'
        self.assertTrue(self.validador_tec.dni(dni))

    def test_dni_none(self):
        dni = None
        self.assertTrue(self.validador_tec.dni(dni))

    def test_dni_fuera_rango(self):
        dni = '100000000'
        self.assertFalse(self.validador_tec.dni(dni))

    def test_dni_caracteres(self):
        dni = '123456T01'
        self.assertFalse(self.validador_tec.dni(dni))

    def test_dni_negativo(self):
        dni = '-34565301'
        self.assertFalse(self.validador_tec.dni(dni))

class TestValidadorDatosSupervisor():
    validador_sup = ValidadorDatosSupervisor()

     # ------------------ validacion de id sucursal ------------------ #
    def test_sucursal_valida(self):
        sucursal_supervisor = "S002"
        self.assertTrue(self.validador_sup.sucursal(sucursal_supervisor))
    
    def test_sucursal_None(self):
        sucursal_supervisor = None
        self.assertFalse(self.validador_sup.sucursal(sucursal_supervisor))

    def test_sucursal_longitud_invalida_1(self):
        sucursal_supervisor = "S0001"
        self.assertFalse(self.validador_sup.sucursal(sucursal_supervisor))

    def test_sucursal_longitud_invalida_2(self):
        sucursal_supervisor = "S01"
        self.assertFalse(self.validador_sup.sucursal(sucursal_supervisor))

    def test_sucursal_caracter_invalido(self):
        sucursal_supervisor = "T001"
        self.assertFalse(self.validador_sup.sucursal(sucursal_supervisor))

    def test_sucursal_ultcaracteres_nodigitos(self):
        sucursal_supervisor = "TBB1"
        self.assertFalse(self.validador_sup.sucursal(sucursal_supervisor)) """