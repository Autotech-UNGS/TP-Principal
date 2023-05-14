import factory
from faker import Faker
import random

faker = Faker()

class Usuario:
    def __init__(self, id_empleado, nombre_completo, dni, nombre_usuario, contrasena, tipo, branch, id_contacto, id_direccion, categoria=None):
        self.id_empleado = id_empleado
        self.nombre_completo = nombre_completo
        self.dni = dni
        self.nombre_usuario = nombre_usuario
        self.categoria = categoria
        self.contrasena = contrasena
        self.tipo = tipo
        self.branch = branch
        self.id_contacto = id_contacto
        self.id_direccion = id_direccion

class UsuarioFactory(factory.Factory):
    class Meta:
        model = Usuario

    @factory.sequence
    def id_empleado(n):
        return n + 1

    @factory.lazy_attribute
    def nombre_completo(self):
        return faker.name()

    @factory.lazy_attribute
    def dni(self):
         return str(random.randint(10000000, 99999999)).zfill(8)

    @factory.lazy_attribute
    def nombre_usuario(self):
        return self.nombre_completo.lower().replace(" ", "")

    @factory.lazy_attribute
    def contrasena(self):
        return faker.password()

    @factory.lazy_attribute
    def tipo(self):
        return faker.random_element(elements=('Tecnico', 'Supervisor'))

    @factory.lazy_attribute
    def branch(self):
        return 'T001' if self.tipo == 'Tecnico' else 'S001'

    @factory.sequence
    def id_contacto(n):
        return n + 1

    @factory.sequence
    def id_direccion(n):
        return n + 1