import pytest
from datetime import date, time
from turnos.validaciones_views import *

# ----------- horarios_exactos ----------- #
def test_horarios_exactos_1():
    assert horarios_exactos(time(3,0,0), time(4,0,0)) == True
    
def test_horarios_exactos_2():
    assert horarios_exactos(time(3,45,0), time(4,0,0)) == False
    
def test_horarios_exactos_3():
    assert horarios_exactos(time(3,0,0), time(4,45,0)) == False
    
def test_horarios_exactos_4():
    assert horarios_exactos(time(3,0,33), time(4,0,0)) == False
    
def test_horarios_exactos_5():
    assert horarios_exactos(time(3,0,0), time(4,0,33)) == False
    
def test_horarios_exactos_6():
    assert horarios_exactos(time(3,46,33), time(4,23,33)) == False
    
def test_horarios_exactos_7():
    assert horarios_exactos(time(3,1,0), time(4,0,0)) == False
    
def test_horarios_exactos_8():
    assert horarios_exactos(time(3,0,0), time(4,1,0)) == False

# ----------- horarios_dentro_de_rango ----------- #
# Domingo
def test_horarios_dentro_de_rango_1():
    assert horarios_dentro_de_rango(date(2023,5,14),time(11, 0, 0), time(12, 0, 0)) == True
    
# empiezan antes/ terminan tarde    
def test_horarios_dentro_de_rango_2():
    assert horarios_dentro_de_rango(date(2023,5,14),time(3, 0, 0), time(12, 0, 0)) == False
    
def test_horarios_dentro_de_rango_3():
    assert horarios_dentro_de_rango(date(2023,5,14),time(12, 0, 0), time(13, 0, 0)) == False
    
def test_horarios_dentro_de_rango_4():
    assert horarios_dentro_de_rango(date(2023,5,14),time(7, 0, 0), time(13, 0, 0)) == False

# Miercoles
def test_horarios_dentro_de_rango_5():
    assert horarios_dentro_de_rango(date(2023,5,10),time(16, 0, 0), time(17, 0, 0)) == True
    
# empiezan antes/ terminan tarde    
def test_horarios_dentro_de_rango_6():
    assert horarios_dentro_de_rango(date(2023,5,10),time(7, 0, 0), time(13, 0, 0)) == False 
    
def test_horarios_dentro_de_rango_7():
    assert horarios_dentro_de_rango(date(2023,5,10),time(12, 0, 0), time(18, 0, 0)) == False
    
def test_horarios_dentro_de_rango_8():
    assert horarios_dentro_de_rango(date(2023,5,10),time(7, 0, 0), time(18, 0, 0)) == False
    
# ----------- dia_valido ----------- #
def test_dia_valido_1():
    assert dia_valido(date(2150, 2, 26)) == True

def test_dia_valido_2():
    assert dia_valido(date(1950, 2, 26)) == False
