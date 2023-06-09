from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .validadores import *

# ----------------------------------------------------------------------------------------------------#
class Taller(models.Model):
    id_taller = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, validators=[nombre_taller_regex])
    direccion = models.CharField(max_length=30)
    localidad = models.CharField(max_length=30)
    provincia = models.CharField(max_length=30)
    cod_postal = models.CharField(max_length=4)
    mail = models.EmailField()
    telefono = models.CharField(max_length=15, validators=[telefono_regex])
    capacidad = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(15)])
    cant_tecnicos = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(45)])
    id_sucursal = models.IntegerField(validators=[MinValueValidator(0)])
    estado = models.BooleanField(default=False)

# ----------------------------------------------------------------------------------------------------#
class Turno_taller(models.Model):
    id_turno = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=14, choices=TiposTurno.choices, default=TiposTurno.SERVICE)
    estado = models.CharField(max_length=10, choices=EstadoTurno.choices, default=EstadoTurno.EN_PROCESO)
    taller_id = models.ForeignKey(Taller, on_delete=models.PROTECT)
    tecnico_id = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(999)], null=True, blank=True)
    patente = models.CharField(max_length=7, validators=[patente_regex])
    fecha_inicio = models.DateField(max_length=10)
    hora_inicio = models.TimeField(max_length=8)
    fecha_fin = models.DateField(max_length=10)
    hora_fin = models.TimeField(max_length=8)
    frecuencia_km = models.IntegerField(validators=[MinValueValidator(5000), MaxValueValidator(200000)]
                                        , choices=Frecuencia_km.choices, null=True, blank=True)
    papeles_en_regla = models.BooleanField(default=True)

# ----------------------------------------------------------------------------------------------------#
class Registro_reparacion(models.Model):
    id_turno = models.OneToOneField(Turno_taller, on_delete=models.PROTECT, primary_key=True)
    tasks_hechas = models.JSONField(null=True, blank=True)
    tasks_pendientes = models.JSONField(null=True, blank=True)
    costo_total = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000000)], default=0.0)
    duracion_total = models.IntegerField(validators=[MinValueValidator(0)])
    fecha_registro = models.DateField(auto_now_add=True)
    detalle = models.TextField(blank=True, null=True)
    detalle_evaluacion = models.TextField(blank=True, null=True)
    origen = models.TextField(choices=OrigenReparacion.choices, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=EstadoRegistroReparacion.choices, default=EstadoRegistroReparacion.EN_PROCESO)
# ----------------------------------------------------------------------------------------------------#
class Registro_extraordinario(models.Model): 
    id_turno = models.OneToOneField(Turno_taller, on_delete=models.PROTECT)
    id_tasks = models.JSONField()
    detalle = models.TextField(blank=True, null=True)
    
# ----------------------------------------------------------------------------------------------------#
class Registro_evaluacion_para_admin(models.Model):
    id_turno = models.OneToOneField(Turno_taller, on_delete=models.PROTECT)
    costo_total = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000000)], default=0.0)
    duracion_total_reparaciones = models.IntegerField(validators=[MinValueValidator(0)], default= 0)
    puntaje_total = models.IntegerField(validators=[MinValueValidator(-2500), MaxValueValidator(2500)], default=2500)
    detalle = models.TextField(blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True)

# ----------------------------------------------------------------------------------------------------#
class Checklist_evaluacion(models.Model):
    id_task = models.AutoField(primary_key=True)
    elemento = models.TextField()
    tarea = models.TextField()
    costo_reemplazo = models.FloatField(validators=[MinValueValidator(0)])
    duracion_reemplazo = models.IntegerField(validators=[MinValueValidator(0)])
    puntaje_max = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2500)], default = 2500)

class Registro_evaluacion(models.Model):
    id_turno = models.OneToOneField(Turno_taller, on_delete=models.PROTECT)
    id_task_puntaje = models.JSONField(null=True, blank=True)
    detalle = models.TextField(blank=True, null=True)

# ----------------------------------------------------------------------------------------------------#
class Cobro_x_hora(models.Model):
    puesto = models.CharField(max_length=30)
    categoria = models.CharField(max_length=1, blank=True, null= True)
    cobro_x_hora = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(3800.0)])

# ----------------------------------------------------------------------------------------------------#
class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    frecuencia_km = models.IntegerField(validators=[MinValueValidator(0)])
    costo_base = models.FloatField(validators=[MinValueValidator(0)])
    costo_total = models.FloatField(validators=[MinValueValidator(costo_base)], default=costo_base)
    duracion_total = models.PositiveIntegerField()
    fecha_creacion = models.DateField(auto_now_add=True)
    id_supervisor = models.PositiveIntegerField()
    activo = models.BooleanField(default=False)

class Registro_service(models.Model):
    id_registro = models.AutoField(primary_key=True)
    id_turno = models.ForeignKey(Turno_taller, on_delete=models.PROTECT)
    id_service = models.ForeignKey(Service, on_delete=models.PROTECT)
    costo_total = models.FloatField(validators=[MinValueValidator(0)])
    duracion_total = models.PositiveIntegerField()
    fecha_registro =  models.DateField(auto_now_add=True)
    garantia = models.BooleanField(default=False)
    id_tasks_reemplazadas = models.JSONField()


class Service_tasks(models.Model):
    id_id_tasks = models.AutoField(primary_key=True)
    id_service = models.ForeignKey(Service,on_delete=models.CASCADE)
    id_tasks = models.JSONField()

class Checklist_service(models.Model):
    id_task = models.AutoField(primary_key=True)
    elemento = models.TextField()
    tarea = models.TextField()
    costo_reemplazo = models.FloatField(validators=[MinValueValidator(0)])
    duracion_reemplazo = models.IntegerField(validators=[MinValueValidator(0)])

# ----------------------------------------------------------------------------------------------------#

