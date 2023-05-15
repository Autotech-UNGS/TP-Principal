
class ValidadorSupervisor():

    def sucursal(sucursal_supervisor):
        if sucursal_supervisor is None:
            return False
        if len(sucursal_supervisor) != 4:
            return False
        if sucursal_supervisor[0] != 'S':
            return False
        if not sucursal_supervisor[1:].isdigit():
            return False   
        return True
