from rest_framework import serializers
from .models import Taller,Turno_taller, Checklist_reparacion, Registro_reparacion, Registro_evaluacion_admin, Id_task_puntaje, Registro_evaluacion


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

class RegistroEvaluacionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_evaluacion_admin
        fields = '__all__'

class RegistroEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_evaluacion
        fields = '__all__'

