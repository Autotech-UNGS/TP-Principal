from django.contrib import admin
from .models import *

# Register your models here

class turno_tallerADMIN(admin.ModelAdmin):
    list_display = ('id_turno', 'tipo', 'estado', 'taller_id', 'tecnico_id', 'patente',
    'fecha_inicio', 'hora_inicio', 'fecha_fin', 'hora_fin','frecuencia_km', 'papeles_en_regla')

class registro_evaluacion_adminADMIN(admin.ModelAdmin):
    list_display = ('id_turno', 'costo_total', 'duracion_total_reparaciones', 'puntaje_total', 'detalle', 'fecha_registro')


class checklist_evaluacionADMIN(admin.ModelAdmin):
    list_display = ('id_task','elemento','tarea','costo_reemplazo','duracion_reemplazo','puntaje_max')


class registro_evaluacionADMIN(admin.ModelAdmin):
    list_display = ('id_turno','id_task_puntaje')

# --------------------------------------------------------------------------------------------------------------------------
admin.site.register(Turno_taller,turno_tallerADMIN)
admin.site.register(Registro_evaluacion_para_admin,registro_evaluacion_adminADMIN)
admin.site.register(Registro_evaluacion,registro_evaluacionADMIN)
admin.site.register(Checklist_evaluacion,checklist_evaluacionADMIN)
