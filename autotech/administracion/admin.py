from django.contrib import admin
from .models import *

# Register your models here.
class tallerADMIN(admin.ModelAdmin):
    list_display = ('id_taller', 'nombre', 'direccion','localidad','provincia','cod_postal', 'mail', 'telefono',
    'capacidad', 'cant_tecnicos')

class turno_tallerADMIN(admin.ModelAdmin):
    list_display = ('id_turno', 'tipo', 'estado', 'taller_id', 'tecnico_id', 'patente',
    'fecha_inicio', 'hora_inicio', 'fecha_fin', 'hora_fin','frecuencia_km', 'papeles_en_regla')

class checklist_reparacionADMIN(admin.ModelAdmin):
    list_display = ('id_task', 'elemento', 'costo', 'duracion')

class registro_reparacionADMIN(admin.ModelAdmin):
    list_display = ('id_registro', 'id_turno', 'tasks_list', 'costo_total', 'duracion_total', 'detalle',
    'fecha_registro')

    def tasks_list(self, obj):
        return ", ".join([task.elemento for task in obj.tasks.all()])

class registro_evaluacion_adminADMIN(admin.ModelAdmin):
    list_display = ('id_turno', 'costo_total', 'duracion_total_reparaciones', 'puntaje_total', 'detalle', 'fecha_registro')


class checklist_evaluacionADMIN(admin.ModelAdmin):
    list_display = ('id_task','elemento','tarea','costo_reemplazo','duracion_reemplazo','puntaje_max')


class id_task_puntajeADMIN(admin.ModelAdmin):
    list_display = ('id_turno','id_task', 'puntaje_seleccionado')

class registro_evaluacionADMIN(admin.ModelAdmin):
    list_display = ('id_turno','id_task_puntaje')


admin.site.register(Checklist_reparacion,checklist_reparacionADMIN)
admin.site.register(Registro_reparacion,registro_reparacionADMIN)

admin.site.register(Taller,tallerADMIN)
admin.site.register(Turno_taller,turno_tallerADMIN)

admin.site.register(Registro_evaluacion_admin,registro_evaluacion_adminADMIN)

admin.site.register(Id_task_puntaje,id_task_puntajeADMIN)
admin.site.register(Registro_evaluacion,registro_evaluacionADMIN)
admin.site.register(Checklist_evaluacion,checklist_evaluacionADMIN)
