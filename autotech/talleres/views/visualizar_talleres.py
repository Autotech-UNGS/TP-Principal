from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from administracion.models import *
from administracion.serializers import TallerSerializer
from rest_framework.response import Response
from datetime import *

class VisualizarTalleresViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def talleresList(self, request):
        turnos= Taller.objects.all()
        serializer= TallerSerializer(turnos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def talleresDetalle(self, request, id_taller):
        try:
            taller=Taller.objects.get(id_taller=id_taller)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        else:
            serializer= TallerSerializer(taller,many=False)
            return Response(serializer.data)