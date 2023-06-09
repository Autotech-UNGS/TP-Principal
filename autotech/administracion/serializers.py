from rest_framework import serializers
from .models import *


class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = '__all__'
# ----------------------------------------------------------------------------------------------------#
class TurnoTallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno_taller
        fields = '__all__'
# ----------------------------------------------------------------------------------------------------#
class RegistroReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_reparacion
        fields = '__all__'

class RegistroExtraordinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_extraordinario
        fields = '__all__'
# ----------------------------------------------------------------------------------------------------#
class RegistroEvaluacionXAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_evaluacion_para_admin
        fields = '__all__'

class RegistroEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_evaluacion
        fields = '__all__'

class ChecklistEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist_evaluacion
        fields = '__all__'
# ----------------------------------------------------------------------------------------------------#
class CobroXHoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobro_x_hora
        fields = '__all__'
# ----------------------------------------------------------------------------------------------------#
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class RegistroServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_service
        fields = '__all__'

class ServiceTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_tasks
        fields = '__all__'

class ChecklistServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist_service
        fields = '__all__'
# ----------------------------------------------------------------------------------------------------#