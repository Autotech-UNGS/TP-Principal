import pytest
from turnos.gestion_agenda.gestionar_agenda import *

# 2023/09/21 --> jueves
def test_duracion_mismo_dia():
    resultado = calcular_duracion(date(2023, 9, 21), time(10,0,0), date(2023,9,21), time(12,0,0))
    assert resultado == 2

# 2023/09/21 --> jueves
# 2023/09/22 --> viernes
def test_duracion_un_dia_mas():
    resultado = calcular_duracion(date(2023, 9, 21), time(10,0,0), date(2023,9,22), time(12,0,0))
    assert resultado == 11
    
# 2023/09/21 --> jueves
# 2023/09/22 --> viernes
# 2023/09/23 --> sabado
def test_duracion_dos_dias_mas():
    resultado = calcular_duracion(date(2023, 9, 21), time(10,0,0), date(2023,9,23), time(12,0,0))
    assert resultado == 20
    
    
# 2023/09/24 --> domingo
def test_duracion_mismo_dia_domingo():
    resultado = calcular_duracion(date(2023, 9, 24), time(8,0,0), date(2023,9,24), time(12,0,0))
    assert resultado == 4

# 2023/09/24 --> domingo
# 2023/09/25 --> lunes
def test_duracion_un_dia_mas_domingo():
    resultado = calcular_duracion(date(2023, 9, 24), time(10,0,0), date(2023,9,25), time(12,0,0))
    assert resultado == 6
    
# 2023/09/24 --> domingo
# 2023/09/25 --> lunes
# 2023/09/26 --> martes
def test_duracion_dos_dias_mas_domingo():
    resultado = calcular_duracion(date(2023, 9, 24), time(10,0,0), date(2023,9,26), time(12,0,0))
    assert resultado == 15