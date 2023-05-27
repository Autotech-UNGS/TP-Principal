from django.urls import reverse
from .test_setup import TestSetUp
from administracion.models import Turno_taller
from turnos.crear_turnos_views import *
from test.factories.usuario_factorie import *

class DiasHorariosDisponiblesTestCase(TestSetUp):
    taller_valido = 100
    taller_invalido = 200
    taller_con_turnos = 101
    
    def get_response_dias_horarios_disponibles(self, taller_id):
        url = reverse('dias-horarios-disponibles', args=[taller_id])
        return self.client.get(url)
    
    def get_response_dias_horarios_disponibles_service(self, taller_id, marca, modelo, km):
        url = reverse('dias-horarios-disponibles-service', args=[taller_id, marca, modelo, km])
        return self.client.get(url)

    def get_response_dias_horarios_disponibles_reparaciones(self, taller_id, patente, origen):
        url = reverse('dias-horarios-disponibles-reparaciones', args=[taller_id, patente, origen])
        return self.client.get(url)    
    
    def generar_response_treinta_dias_completo(self):
        dias_horarios = []
        dia = date.today()
        for i in range(32):
            dia_horario = {"dia": dia.strftime("%Y-%m-%d"), "horarios_disponibles": self.obtener_horarios(dia)}
            dias_horarios.append(dia_horario)
            dia = dia + timedelta(days=1)        
        resultado = {'dias_y_horarios': dias_horarios}            
        return resultado
    
    def generar_response_cuarentaycinco_dias_completo(self):
        dias_horarios = []
        dia = date.today()
        for i in range(47):
            dia_horario = {"dia": dia.strftime("%Y-%m-%d"), "horarios_disponibles": self.obtener_horarios(dia)}
            dias_horarios.append(dia_horario)
            dia = dia + timedelta(days=1)        
        resultado = {'dias_y_horarios': dias_horarios}            
        return resultado

    def obtener_horarios(self, dia:date):
        ultimo_horario = 17 if dia.weekday() != 6 else 12
        if dia != date.today() or (dia == date.today() and datetime.now().hour < 8):
            hora = 8
        elif datetime.now().hour > ultimo_horario:
            return []
        else:
            hora = datetime.now().hour - 2 # esto para que ande en la api
        horas = []
        while hora < ultimo_horario:
            horas.append(hora)
            hora += 1
        return horas
    
# ----------------------------------------------------------------------------------- #    
# ------------------------------------- una hora ------------------------------------ #
# ----------------------------------------------------------------------------------- #    

    def test_una_hora_completo(self):
        response_esperado = self.generar_response_treinta_dias_completo()
        
        response = self.get_response_dias_horarios_disponibles(self.taller_valido)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado) 
        
    def test_una_hora_incompleto(self):
        response_esperado = self.generar_response_treinta_dias_completo()
        posicion = next((index for index, item in enumerate(response_esperado["dias_y_horarios"]) if item["dia"] == "2023-06-27"), None)
        response_esperado["dias_y_horarios"][posicion]['horarios_disponibles'] = [9,11,12,13,14,16]
        
        response = self.get_response_dias_horarios_disponibles(self.taller_con_turnos)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado) 
    
        
    def test_una_hora_taller_no_existe(self):
        self.assertEqual(self.get_response_dias_horarios_disponibles(self.taller_invalido).status_code, 400)
# ----------------------------------------------------------------------------------- #    
# ------------------------------------- service ------------------------------------- #
# ----------------------------------------------------------------------------------- #           
        
    def test_service_completo(self):
        response_esperado = self.generar_response_treinta_dias_completo()
        
        response = self.get_response_dias_horarios_disponibles_service(self.taller_valido, "generico", "generico", 5000)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)         
        
    def test_service_incompleto(self):
        response_esperado = self.generar_response_treinta_dias_completo()
        posicion = next((index for index, item in enumerate(response_esperado["dias_y_horarios"]) if item["dia"] == "2023-06-27"), None)
        response_esperado["dias_y_horarios"][posicion - 1]['horarios_disponibles'] = [8,9,10,11,12,13,14] # el 15 y 16 no, porque al otro dia, a las 8 estamos ocupados
        response_esperado["dias_y_horarios"][posicion]['horarios_disponibles'] = [11,12,16]
        
        response = self.get_response_dias_horarios_disponibles_service(self.taller_con_turnos, 'generico', 'generico', 5000) # este service dura 3 horas
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)         
        
    def test_service_no_existe(self): 
        self.assertEqual(self.get_response_dias_horarios_disponibles_service(self.taller_valido, "Ford", "Ka", 5000).status_code, 400) 
        
    def test_service_taller_no_existe(self):
        self.assertEqual(self.get_response_dias_horarios_disponibles_service(self.taller_invalido, "generico", "generico", 5000).status_code, 400)     
              
# ----------------------------------------------------------------------------------- #    
# ------------------------------ reparacion: evaluacion ----------------------------- #
# ----------------------------------------------------------------------------------- #                 
    
    def test_reparaciones_evaluacion_completo(self):
        response_esperado = self.generar_response_cuarentaycinco_dias_completo()
        
        response = self.get_response_dias_horarios_disponibles_reparaciones(self.taller_valido, "LCS262", "evaluacion")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)  
        
    def test_reparaciones_evaluacion_incompleto(self):
        response_esperado = self.generar_response_cuarentaycinco_dias_completo()
        posicion = next((index for index, item in enumerate(response_esperado["dias_y_horarios"]) if item["dia"] == "2023-06-27"), None)
        response_esperado["dias_y_horarios"][posicion - 1]['horarios_disponibles'] = [8,9,10,11,12,13,14] # el 15 y 16 no, porque al otro dia, a las 8 estamos ocupados
        response_esperado["dias_y_horarios"][posicion]['horarios_disponibles'] = [11,12,16]
        
        response = self.get_response_dias_horarios_disponibles_reparaciones(self.taller_con_turnos, "LCS262", "evaluacion") # esta reparacion dura 3 horas
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)        
    
    def test_reparaciones_evaluacion_taller_no_existe(self):   
        self.assertEqual(self.get_response_dias_horarios_disponibles_reparaciones(self.taller_invalido, "LCS262", "evaluacion").status_code, 400)  
        
    def test_reparaciones_evaluacion_vehiculo_no_evaluado(self):
        self.assertEqual(self.get_response_dias_horarios_disponibles_reparaciones(self.taller_valido, "CBS291", "evaluacion").status_code, 400)
        
# ----------------------------------------------------------------------------------- #    
# ---------------------------- reparacion: extraordinario --------------------------- #
# ----------------------------------------------------------------------------------- #         
        
    def test_reparaciones_extraordinario_completo(self):
        response_esperado = self.generar_response_cuarentaycinco_dias_completo()
        
        response = self.get_response_dias_horarios_disponibles_reparaciones(self.taller_valido, "LCS262", "extraordinario")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)
        
    def test_reparaciones_extraordinario_incompleto(self):
        response_esperado = self.generar_response_cuarentaycinco_dias_completo()
        posicion = next((index for index, item in enumerate(response_esperado["dias_y_horarios"]) if item["dia"] == "2023-06-27"), None)
        response_esperado["dias_y_horarios"][posicion - 1]['horarios_disponibles'] = [8,9,10,11,12,13,14,15] # el 16 no, porque al otro dia, a las 8 estamos ocupados
        response_esperado["dias_y_horarios"][posicion]['horarios_disponibles'] = [11,12,13,16]
        
        response = self.get_response_dias_horarios_disponibles_reparaciones(self.taller_con_turnos, "LCS262", "extraordinario") # esta reparacion dura 2 horas
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_esperado)         
        
    def test_reparaciones_extraordinario_taller_no_existe(self):
        self.assertEqual(self.get_response_dias_horarios_disponibles_reparaciones(self.taller_invalido, "LCS262", "extraordinario").status_code, 400)      
        
    def test_reparaciones_extraordinario_vehiculo_no_evaluado(self):
        self.assertEqual(self.get_response_dias_horarios_disponibles_reparaciones(self.taller_valido, "CBS291", "extraordinario").status_code, 400) 
        
    