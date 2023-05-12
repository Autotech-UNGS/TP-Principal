import pytest
from asignar_tecnico import * 
from administracion.models import Turno_taller
from datetime import date, time

# ----------------- se puede asignar ----------------- #

def test_se_puede_asignar_tecnico_1():
    # papeles en orden --> True
    assert se_puede_asignar_tecnico("Evaluacion", True) == True
    
    
def test_se_puede_asignar_tecnico_2():
    # papeles no en orden --> False
    assert se_puede_asignar_tecnico("Evaluacion", False) == False
    
def test_se_puede_asignar_tecnico_3():
    # tipo == Service --> True
    assert se_puede_asignar_tecnico("Service", False) == True
    
def test_se_puede_asignar_tecnico_4():
    # tipo == Extraordinario --> True
    assert se_puede_asignar_tecnico("Extraordinario", False) == True    
    
def test_se_puede_asignar_tecnico_5():
    # tipo == Reparacion --> True
    assert se_puede_asignar_tecnico("Reparacion", False) == True

# ----------------- esta disponible ----------------- #

@pytest.mark.django_db
def test_esta_disponible_1():
    # tecnico con turnos ese dia, esta disponible ese horario
    id_tecnico = 5
    dia = date(2023,5,11)
    hora_inicio = time(13,0,0)
    hora_fin = time(14,0,0)
    
    assert esta_disponible(id_tecnico,dia, hora_inicio, hora_fin) == True

@pytest.mark.django_db    
def test_esta_disponible_2():
    # tecnico con turnos ese dia, no esta disponible ese horario
    id_tecnico = 5
    dia = date(2023,5,11)
    hora_inicio = time(11,0,0)
    hora_fin = time(12,0,0)
    
    assert esta_disponible(id_tecnico,dia, hora_inicio, hora_fin) == False   

@pytest.mark.django_db    
def test_esta_disponible_3():
    # tecnico con turnos otro dia, esta disponible ese horario
    id_tecnico = 5
    dia = date(2023,5,15)
    hora_inicio = time(9,0,0)
    hora_fin = time(10,0,0)
    
    assert esta_disponible(id_tecnico,dia, hora_inicio, hora_fin) == True 
    
@pytest.mark.django_db    
def test_esta_disponible_4():
    # tecnico sin turnos, esta disponible ese horario
    id_tecnico = 55
    dia = date(2023,5,11)
    hora_inicio = time(11,0,0)
    hora_fin = time(12,0,0)
    
    assert esta_disponible(id_tecnico,dia, hora_inicio, hora_fin) == True 
    
@pytest.mark.django_db
def test_esta_disponible_5():
    # tecnico con turnos ese dia, (superposición) no esta disponible ese horario
    id_tecnico = 5
    dia = date(2023,11,5)
    hora_inicio = time(10,0,0)
    hora_fin = time(13,0,0)
    
    assert esta_disponible(id_tecnico,dia, hora_inicio, hora_fin) == False

# ----------------- hay superposicion ----------------- #

def test_hay_superposicion_1():
    # no se relacionan en nada --> no hay
    hora_inicio_2 = time(11,0,0)
    hora_fin_2 = time(12,0,0)
    hora_inicio_1 = time(14,0,0)
    hora_fin_1 = time(15,0,0)
    
    assert no_hay_superposicion(hora_inicio_1, hora_fin_1, hora_inicio_2, hora_fin_2) == True 

def test_hay_superposicion_2():
    # uno empieza cuando el otro termina --> no hay
    hora_inicio_1 = time(11,0,0)
    hora_fin_1 = time(12,0,0)
    hora_inicio_2 = time(12,0,0)
    hora_fin_2 = time(13,0,0)
    
    assert no_hay_superposicion(hora_inicio_1, hora_fin_1, hora_inicio_2, hora_fin_2) == True
    

def test_hay_superposicion_3():
    # uno termina cuando el otro empieza --> no hay
    hora_inicio_2 = time(11,0,0)
    hora_fin_2 = time(12,0,0)
    hora_inicio_1 = time(12,0,0)
    hora_fin_1 = time(13,0,0)
    
    assert no_hay_superposicion(hora_inicio_1, hora_fin_1, hora_inicio_2, hora_fin_2) == True   
    
def test_hay_superposicion_4():
    # uno empieza durante el otro turno --> si hay
    hora_inicio_2 = time(11,0,0)
    hora_fin_2 = time(13,0,0)
    hora_inicio_1 = time(12,0,0)
    hora_fin_1 = time(13,0,0)
    
    assert no_hay_superposicion(hora_inicio_1, hora_fin_1, hora_inicio_2, hora_fin_2) == False  
    
def test_hay_superposicion_5():
    # uno empieza a la vez que el otro turno --> si hay
    hora_inicio_2 = time(11,0,0)
    hora_fin_2 = time(12,0,0)
    hora_inicio_1 = time(11,0,0)
    hora_fin_1 = time(13,0,0)
    
    assert no_hay_superposicion(hora_inicio_1, hora_fin_1, hora_inicio_2, hora_fin_2) == False
    
def test_hay_superposicion_6():
    # son iguales --> si hay
    hora_inicio_2 = time(11,0,0)
    hora_fin_2 = time(12,0,0)
    hora_inicio_1 = time(11,0,0)
    hora_fin_1 = time(12,0,0)
    
    assert no_hay_superposicion(hora_inicio_1, hora_fin_1, hora_inicio_2, hora_fin_2) == False
    