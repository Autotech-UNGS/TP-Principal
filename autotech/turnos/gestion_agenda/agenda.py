from datetime import date, timedelta, datetime

class Agenda:
    
    def __init__(self, capacidad:int) -> None:
        self.dias_horarios = {} #date->[[8, capacidad], [9, capacidad], [10, capacidad],...]
        self.capacidad = capacidad
        self.comienzo_horario_de_trabajo= 8
        self.fin_horario_de_trabajo= 17
        self.fin_horario_de_trabajo_domingos= 12
                  
    def esta_disponible(self, dia:date, horario:int, duracion:int) -> bool:
        hora = horario
        fecha = dia
        horarios_del_dia = self.obtener_horarios_del_dia(fecha)  #[[8,capacidad],[9,capacidad]]
        for i in range(duracion):
            if (hora == self.fin_horario_de_trabajo and fecha.weekday() != 6) or (hora == self.fin_horario_de_trabajo_domingos and fecha.weekday() == 6):
                hora = 8
                fecha = fecha + timedelta(days=1)
                horarios_del_dia = self.obtener_horarios_del_dia(fecha)  #[[8,capacidad],[9,capacidad]]                
            if horarios_del_dia[hora - 8][1] == 0:
                return False
            hora+=1
        return True
        
    def obtener_horarios_del_dia(self, dia:date) -> list:
        horarios_del_dia = self.dias_horarios.get(dia)
        if horarios_del_dia == None:
            self.inicializar_horarios(dia)
        return self.dias_horarios.get(dia)    
    
    def horarios_capacidad(self, dia:date) -> list:   # [horarios disponibles]
        horarios_del_dia = self.obtener_horarios_del_dia(dia)
        horarios_disponibles = []
        for hora in horarios_del_dia: #[8,capacidad], [9, capacidad], ...
            horarios_disponibles.append(hora) # [8, capacidad] --> [8]
        return horarios_disponibles

    def dias_horarios_disponibles_de_treinta_dias(self, dia:date, cant_horas: int) -> dict:  #{date -> [horarios disponibles]}
        dias_horarios_disponibles = {}
        dia_a_revisar = dia
        for i in range(32):
            horarios_disponibles = self.horarios_disponibles(dia_a_revisar, cant_horas)
            dias_horarios_disponibles[dia_a_revisar]= horarios_disponibles
            dia_a_revisar = dia_a_revisar + timedelta(days=1)
        return dias_horarios_disponibles
    
    def dias_horarios_disponibles_de_cuarentaycinco_dias(self, dia:date, cant_horas: int) -> dict:  #{date -> [horarios disponibles]}
        dias_horarios_disponibles = {}
        dia_a_revisar = dia
        for i in range(47):
            horarios_disponibles = self.horarios_disponibles(dia_a_revisar, cant_horas)
            dias_horarios_disponibles[dia_a_revisar]= horarios_disponibles
            dia_a_revisar = dia_a_revisar + timedelta(days=1)
        return dias_horarios_disponibles
                
    def horarios_disponibles(self, dia, cant_horas):
        horarios_del_dia = self.obtener_horarios_del_dia(dia)
        horarios_disponibles = []
        hoy = date.today()
        ahora = datetime.now().time()
        for hora in horarios_del_dia:
            if (dia != hoy or ( dia == hoy and hora[0] > ahora.hour - 3)) and hora[1] > 0:
                if self.esta_disponible(dia, hora[0], cant_horas):
                    horarios_disponibles.append(hora[0])
        
        return horarios_disponibles
    
    
    def cargar_turno(self, dia:date, hora_inicio:int, duracion:int):
        if not self.esta_disponible(dia, hora_inicio, duracion):
            raise ValueError("error: no hay espacio disponible para ese turno")
        horarios_del_dia = self.obtener_horarios_del_dia(dia)
        fecha = dia
        hora = hora_inicio
        for i in range(duracion):
            if (hora == self.fin_horario_de_trabajo and fecha.weekday() != 6) or (hora == self.fin_horario_de_trabajo_domingos and fecha.weekday() == 6):
                hora = 8
                fecha = fecha + timedelta(days=1)
                horarios_del_dia = self.obtener_horarios_del_dia(fecha)  #[[8,capacidad],[9,capacidad]]
            horarios_del_dia[hora - 8][1] = horarios_del_dia[hora - 8][1] - 1
            hora += 1
                
        
    def inicializar_horarios(self, dia:date):
        dia_de_la_semana = dia.weekday()
        horas = []
        if dia_de_la_semana != 6:
            for i in range(self.comienzo_horario_de_trabajo, self.fin_horario_de_trabajo):
                hora = [i, self.capacidad]
                horas.append(hora)
        else:
            for i in range(self.comienzo_horario_de_trabajo, self.fin_horario_de_trabajo_domingos):
                hora = [i, self.capacidad]
                horas.append(hora)
        self.dias_horarios[dia] = horas
      
    def eliminar_turno(self, dia:date, hora_inicio:int, duracion:int):
        horarios_del_dia = self.obtener_horarios_del_dia(dia)
        fecha = dia
        hora = hora_inicio
        for i in range(duracion):
            horarios_del_dia[hora - 8][1] = horarios_del_dia[hora - 8][1] + 1
            if (hora == self.fin_horario_de_trabajo and fecha.weekday() != 6) or (hora == self.fin_horario_de_trabajo_domingos and fecha.weekday() == 6):
                hora = 7
                fecha = fecha + timedelta(days=1)
                horarios_del_dia = self.obtener_horarios_del_dia(fecha)  #[[8,capacidad],[9,capacidad]]
            hora += 1