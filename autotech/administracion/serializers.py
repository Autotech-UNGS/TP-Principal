from rest_framework import serializers
from .models import *


class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = '__all__'

class TurnoTallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno_taller
        fields = '__all__'

class ChecklistReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist_reparacion
        fields = '__all__'

class RegistroReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_reparacion
        fields = '__all__'

class RegistroEvaluacionXAdminSerializerGET(serializers.ModelSerializer):
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

class CobroXHoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobro_x_hora
        fields = '__all__'