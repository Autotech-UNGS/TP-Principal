
class ValidadorDatosTecnico():
    
    def sucursal(self, sucursal_supervisor):
        if sucursal_supervisor is None:
            return False
        if len(sucursal_supervisor) != 4:
            return False
        if sucursal_supervisor[0] != 'S':
            return False
        if not sucursal_supervisor[1:].isdigit():
            return False   
        return True

    def categoria(self, categoria=None):
        tipos_categorias = ["A", "B", "C", "D"]
        if categoria is not None and categoria not in tipos_categorias:
            return False   
        return True

    def dni(self, dni=None):
        if dni is not None and (not dni.isdigit() or (len(dni) < 7 or len(dni) > 8)):
            return False 
        return True

