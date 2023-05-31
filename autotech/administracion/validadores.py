from django.core.validators import RegexValidator
from django.db import models

nombre_taller_regex = RegexValidator(
        regex='^[a-zA-Z0-9&\s]+$',
        message="El nombre de taller debe contener solo números, letras, espacios y &",
        code="invalid_nombre_taller")

telefono_regex = RegexValidator(
    regex='^\+?1?\d{9,15}$',
    message="El número de teléfono debe tener el formato +1234567890 y contener de 9 a 15 dígitos.",
    code="invalid_phone_number")

patente_regex = RegexValidator(
    '^(([A-Z]{2}\d{3}[A-Z]{2})|([A-Z]{3}\d{3}))$',
    message="La patente ingresada no es valida. Debe ser en mayusculas con el formato 00AAA00 o AAA000 ",
    code="invalid_patente")


class EstadoTurno(models.TextChoices):
    PENDIENTE ="pendiente",("Pendiente")
    RECHAZADO = "rechazado",("Rechazado")
    EN_PROCESO = "en_proceso",("En proceso")
    TERMINADO = "terminado",("Terminado")
    CANCELADO = "cancelado",("Cancelado")
    AUSENTE = "ausente",("Ausente")

class TiposTurno(models.TextChoices):
    SERVICE = "service",("Service")
    EVALUACION ="evaluacion",("Evaluacion")
    EXTRAORDINARIO = "extraordinario",("Extraordinario")
    REPARACION = "reparacion", ("Reparacion")

class Frecuencia_km(models.IntegerChoices):
        FREQ_5000 = 5000, '5.000 KM'
        FREQ_10000 = 10000, '10.000 KM'
        FREQ_15000 = 15000, '15.000 KM'
        FREQ_20000 = 20000, '20.000 KM'
        FREQ_25000 = 25000, '25.000 KM'
        FREQ_30000 = 30000, '30.000 KM'
        FREQ_35000 = 35000, '35.000 KM'
        FREQ_40000 = 40000, '40.000 KM'
        FREQ_45000 = 45000, '45.000 KM'
        FREQ_50000 = 50000, '50.000 KM'
        FREQ_55000 = 55000, '55.000 KM'
        FREQ_60000 = 60000, '60.000 KM'
        FREQ_65000 = 65000, '65.000 KM'
        FREQ_70000 = 70000, '70.000 KM'
        FREQ_75000 = 75000, '75.000 KM'
        FREQ_80000 = 80000, '80.000 KM'
        FREQ_85000 = 85000, '85.000 KM'
        FREQ_90000 = 90000, '90.000 KM'
        FREQ_95000 = 95000, '95.000 KM'
        FREQ_100000 = 100000, '100.000 KM'
        FREQ_105000 = 105000, '105.000 KM'
        FREQ_110000 = 110000, '110.000 KM'
        FREQ_115000 = 115000, '115.000 KM'
        FREQ_120000 = 120000, '120.000 KM'
        FREQ_125000 = 125000, '125.000 KM'
        FREQ_130000 = 130000, '130.000 KM'
        FREQ_135000 = 135000, '135.000 KM'
        FREQ_140000 = 140000, '140.000 KM'
        FREQ_145000 = 145000, '145.000 KM'
        FREQ_150000 = 150000, '150.000 KM'
        FREQ_155000 = 155000, '155.000 KM'
        FREQ_160000 = 160000, '160.000 KM'
        FREQ_165000 = 165000, '165.000 KM'
        FREQ_170000 = 170000, '170.000 KM'
        FREQ_175000 = 175000, '175.000 KM'
        FREQ_180000 = 180000, '180.000 KM'
        FREQ_185000 = 185000, '185.000 KM'
        FREQ_190000 = 190000, '190.000 KM'
        FREQ_195000 = 195000, '195.000 KM'
        FREQ_200000 = 200000, '200.000 KM'

class OrigenReparacion(models.TextChoices):
    EVALUACION ="evaluacion",("Evaluacion")
    EXTRAORDINARIO = "extraordinario",("Extraordinario")

class EstadoTaller(models.TextChoices):
    ACTIVO ="activo",("Activo")
    INACTIVO = "inactivo",("Inactivo")