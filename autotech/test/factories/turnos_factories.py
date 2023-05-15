import factory
from faker import Faker
import random
from administracion.models import Turno_taller

faker = Faker()

class Turno:
    def __init__(self, id_turno, tipo, estado, taller_id, tecnico_id, patente, fecha_inicio, hora_inicio, fecha_fin, hora_fin, frecuencia_km, papeles_en_regla):
        self.id_turno = id_turno
        self.tipo = tipo
        self.estado = estado
        self.taller_id = taller_id
        self.tecnico_id = tecnico_id
        self.patente = patente
        self.fecha_inicio = fecha_inicio
        self.hora_inicio = hora_inicio
        self.fecha_fin = fecha_fin
        self.hora_fin = hora_fin
        self.fecuencia_km = frecuencia_km
        self.papeles_en_regla = papeles_en_regla
    
class TurnoFactory(factory.Factory):
    class Meta:
        model = Turno
        
    @factory.sequence
    def id_turno(n):
        return n + 1
    
    @factory.lazy_attribute
    def tipo(self):
        return faker.random_element(elements=('Evaluacion', 'Service', 'Extraordinario', 'Reparacion'))
    
    @factory.lazy_attribute
    def estado(self):
        return faker.random_element(elements=('Pendiente', 'Rechazado','En proceso', 'Terminado'))
    
    @factory.sequence
    def taller_id(n):
        return n + 1
    
    @factory.sequence
    def tecnico_id(self, n):
        secuencia = n + 1
        return secuencia if self.estado == 'En proceso' else None
    
    @factory.lazy_attribute
    def patente(self):
        numero = str(random.randint(100,999)).zfill(3)
        letras = str(random.choice("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ").zfill(3))
        return numero + letras
    
    @factory.lazy_attribute
    def fecha_inicio(self):
        return factory.Faker('date')
    
    @factory.lazy_attribute
    def hora_inicio(self):
        return factory.Faker('time')
    
    @factory.lazy_attribute
    def fecha_fin(self):
        return factory.Faker('date')
    
    @factory.lazy_attribute
    def hora_fin(self):
        return factory.Faker('time')
    
    @factory.lazy_attribute
    def frecuencia_km(self):
        return faker.random_element(elements=(5000, 10000, 15000, 20000, 25000)) if self.tipo == 'Service' else None
    
    @factory.lazy_attribute
    def papeles_en_regla(self):
        return faker.random_element(elements=(True, False)) if self.tipo == 'Evaluacion' else False