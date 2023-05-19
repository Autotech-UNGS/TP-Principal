from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import *
from .models import *

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
    serializer_class = ChecklistReparacionSerializer
    permission_classes = [permissions.AllowAny]

class RegistroReparacionViewSet(viewsets.ModelViewSet):
    queryset = Registro_reparacion.objects.all()
    serializer_class = RegistroReparacionSerializer
    permission_classes = [permissions.AllowAny] 

class CobroXHoraTodosViewSet(viewsets.ModelViewSet):
    queryset = Cobro_x_hora.objects.all()
    serializer_class = CobroXHoraSerializer
    permission_classes = [permissions.AllowAny] 


class CobroXHoraTecnicosViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CobroXHoraSerializer
    permission_classes = [permissions.AllowAny] 

    def get_queryset(self):
        queryset = Cobro_x_hora.objects.filter(puesto='tecnico')
        return queryset

class CobroXHoraTecnicosCategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CobroXHoraSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Cobro_x_hora.objects.filter(puesto='tecnico')
        categoria = self.kwargs['categoria']
        if categoria:
            categoria = categoria.upper()
            queryset = queryset.filter(categoria=categoria)
        return queryset

class CobroXHoraSupervisorViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CobroXHoraSerializer
    permission_classes = [permissions.AllowAny] 

    def get_queryset(self):
        queryset = Cobro_x_hora.objects.filter(puesto='supervisor')
        return queryset
    
class CobroXHoraTecnicosCategoriaCobroViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, categoria, format=None):
        categoria = categoria.upper()
        cobro_x_hora = Cobro_x_hora.objects.filter(puesto='tecnico', categoria=categoria).values_list('cobro_x_hora', flat=True).first()
        data = {
            'cobro_x_hora': cobro_x_hora
        }
        return Response(data, status=status.HTTP_200_OK)
    

class CobroXHoraCobroViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        cobro_x_hora = Cobro_x_hora.objects.filter(puesto='supervisor').values_list('cobro_x_hora', flat=True).first()
        data = {
            'cobro_x_hora': cobro_x_hora
        }
        return Response(data, status=status.HTTP_200_OK)