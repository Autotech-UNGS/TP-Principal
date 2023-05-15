from administracion.models import Registro_evaluacion_admin, Id_task_puntaje, Registro_evaluacion
from rest_framework import serializers


class RegistroEvaluacionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_evaluacion_admin
        fields = '__all__'

class RegistroEvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_evaluacion
        fields = '__all__'

class IdTaskPuntajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Id_task_puntaje
        fields = '__all__'
