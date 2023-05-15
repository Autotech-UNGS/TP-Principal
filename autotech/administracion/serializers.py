from rest_framework import serializers
from .models import Taller,Turno_taller, Checklist_reparacion, Registro_reparacion


class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = '__all__'


class TurnoTallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno_taller
        fields = '__all__'

class ChecklistReparacionrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist_reparacion
        fields = '__all__'

class RegistroReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_reparacion
        fields = '__all__'