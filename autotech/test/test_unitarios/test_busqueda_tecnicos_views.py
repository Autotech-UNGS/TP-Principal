import pytest
from .views import sucursal_es_valida, categoria_es_valida, dni_es_valido

# ------------------ validacion de id sucursal ------------------ #
def test_sucursal_None():
    sucursal_supervisor = None
    assert sucursal_es_valida(sucursal_supervisor) == False

def test_sucursal_longitud_invalida_1():
    sucursal_supervisor = "S0001"
    assert sucursal_es_valida(sucursal_supervisor) == False

def test_sucursal_longitud_invalida_2():
    sucursal_supervisor = "S01"
    assert sucursal_es_valida(sucursal_supervisor) == False

def test_sucursal_caracter_invalido():
    sucursal_supervisor = "T001"
    assert sucursal_es_valida(sucursal_supervisor) == False

def test_sucursal_ultcaracteres_nodigitos():
    sucursal_supervisor = "TBB1"
    assert sucursal_es_valida(sucursal_supervisor) == False

def test_sucursal_valida():
    sucursal_supervisor = "S002"
    assert sucursal_es_valida(sucursal_supervisor) == True

# ------------------ validacion de categoria tecnico ------------------ #
def test_categoria_none():
    categoria = None
    assert categoria_es_valida(categoria) == True 

def test_categoria_numero():
    categoria = 2
    assert categoria_es_valida(categoria) == False

def test_categoria_minuscula():
    categoria = 'a'
    assert categoria_es_valida(categoria) == False

def test_categoria_inexistente():
    categoria = 'T'
    assert categoria_es_valida(categoria) == False   

def test_categoria_valida():
    categoria = 'D'
    assert categoria_es_valida(categoria) == True   

# ------------------ validacion dni de un tecnico ------------------ #
def test_dni_none():
    dni = None
    assert dni_es_valido(dni) == True

def test_dni_fuera_rango():
    dni = '12345678901'
    assert dni_es_valido(dni) == False

def test_dni_caracteres():
    dni = '123456T01'
    assert dni_es_valido(dni) == False

def test_dni_negativo():
    dni = '-34565301'
    assert dni_es_valido(dni) == False

def test_dni_valido():
    dni = '34565301'
    assert dni_es_valido(dni) == True