from rest_framework import viewsets, permissions
from .serializers import TallerSerializer,TurnoTallerSerializer, ChecklistReparacionrSerializer, RegistroReparacionSerializer
from .models import Taller, Turno_taller, Checklist_reparacion, Registro_reparacion

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    serializer_class = TallerSerializer
    permission_classes = [permissions.AllowAny]

class TurnoTallerViewSet(viewsets.ModelViewSet):
    queryset = Turno_taller.objects.all()
    serializer_class = TurnoTallerSerializer
    permission_classes = [permissions.AllowAny]

class ChecklistReparacionViewSet(viewsets.ModelViewSet):
    queryset = Checklist_reparacion.objects.all()
    serializer_class = ChecklistReparacionrSerializer
    permission_classes = [permissions.AllowAny]

class RegistroReparacionViewSet(viewsets.ModelViewSet):
    queryset = Registro_reparacion.objects.all()
    serializer_class = RegistroReparacionSerializer
    permission_classes = [permissions.AllowAny] 
