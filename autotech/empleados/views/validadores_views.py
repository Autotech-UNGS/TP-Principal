
class ValidadorDatosEmpleado():
    def categoria_tecnico(self, categoria=None):
        tipos_categorias = ["A", "B", "C", "D"]
        if categoria is not None and categoria not in tipos_categorias:
            return False   
        return True

    def dni(self, dni=None):
        if dni is not None and (not dni.isdigit() or (len(dni) < 7 or len(dni) > 8)):
            return False 
        return True
    
    def taller(self, taller_empleado):
        if taller_empleado is None:
            return False
        if len(taller_empleado) != 4:
            return False
        if taller_empleado[0] != 'T':
            return False
        if not taller_empleado[1:].isdigit():
            return False   
        return True

