import json

import requests

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from administracion.models import  Turno_taller, Registro_service, Checklist_service, Service, Service_tasks
from administracion.serializers import TurnoTallerSerializer, RegistroServiceSerializer, ChecklistServiceSerializer
from services import validadores

from vehiculos.api_client.vehiculos import ClientVehiculos




# -----------------------------------------------------------------------------------------------------
#------------------------------------LISTAR REGISTROS DE SERVICE PENDIENTES----------------------------
# -----------------------------------------------------------------------------------------------------
class ListarTurnosRegistroPendienteTecnico(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id_tecnico, format=None):
        
        # El técnico pasado no tiene turnos de service en proceso actualmente 
        """  if not Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='evaluacion'):
            return Response({'error': 'El ID del técnico no es válido con un turno de evaluación vigente'}, status=status.HTTP_400_BAD_REQUEST) """
        
        turnos = Turno_taller.objects.filter(tecnico_id=id_tecnico, estado='en_proceso', tipo='service')
        id_turnos = list(turnos.values_list('id_turno', flat=True))

        # El técnico no tiene registros de service guardados
        if not Registro_service.objects.filter(id_turno__in = id_turnos):
            serializer = TurnoTallerSerializer(turnos, many=True)
            # Si no tiene turnos registrados de service entonces devuelvo todos los turnos que tenga 
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        registros = Registro_service.objects.filter(id_turno__in = id_turnos) 
        id_turnos_registros = list(registros.values_list('id_turno', flat=True))

        turnos_pendientes_de_registro = Turno_taller.objects.filter(id_turno__in = id_turnos).exclude(id_turno__in = id_turnos_registros)
        serializer = TurnoTallerSerializer(turnos_pendientes_de_registro, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO EVALUACION LEER TODOS------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroEvaluacionList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if not Registro_service.objects.exists():
            return Response({'message': 'No hay registros actualmente'}, status=status.HTTP_204_NO_CONTENT)
        else:
            registros = Registro_service.objects.all()
            serializer = RegistroServiceSerializer(registros, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
# -----------------------------------------------------------------------------------------------------
#------------------------------------AUXILIARES DE SERVICE---------------------------------------------
# -----------------------------------------------------------------------------------------------------

def obtener_service(marca,modelo,kilometraje):
    if Service.objects.filter(marca=marca, modelo=modelo, frecuencia_km=kilometraje).exists():
            
        service = Service.objects.get(marca=marca, modelo=modelo, frecuencia_km=kilometraje)
        service_id = service.id_service
        return service_id
    
    elif Service.objects.filter(marca='generico', modelo='generico', frecuencia_km=kilometraje).exists():
        service = Service.objects.get(marca='generico', modelo='generico', frecuencia_km=kilometraje)
        service_id = service.id_service
        return service_id
    else:
        service_id = None
        return service_id

def obtener_costo_final_service(tiene_garantia,id_service, list_tasks_reemplazadas):
    if tiene_garantia:
        service = Service.objects.get(id_service = id_service)
        return service.costo_base
    
    else:
        service = Service.objects.get(id_service = id_service)
        costo_total = service.costo_base

        for id in list_tasks_reemplazadas:
            item = Checklist_service.objects.get(id_task = id)
            costo_total += item.costo_reemplazo
        return costo_total


# -----------------------------------------------------------------------------------------------------
#------------------------------------REGISTRO SERVICE CREAR--------------------------------------------
# -----------------------------------------------------------------------------------------------------
class RegistroServiceCreate(APIView):
    permission_classes = [permissions.AllowAny]
    
    # id_turno, tareas_reparadas [1,2,3,4,5,6]
    
    def post(self, request, *args, **kwargs):

        id_turno = request.data.get('id_turno')

        print(id_turno)
        
        if not id_turno:
            return Response({'error': 'El campo "id_turno" es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        if not Turno_taller.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        turno = Turno_taller.objects.get(id_turno=id_turno)


        if not turno.tipo == "service":
            return Response({'error': 'El turno pasado no es un turno para Service'}, status=status.HTTP_400_BAD_REQUEST)
    
        if not turno.estado == "en_proceso":
            return Response({'error': 'El turno pasado no está en estado en proceso'}, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------OBTENER SERVICE TURNO--------------------------------------------------------------------------
        patente_del_turno = turno.patente
        modelo = ClientVehiculos.obtener_modelo(patente_del_turno)
        marca = ClientVehiculos.obtener_marca(patente_del_turno)
        km_del_turno = turno.frecuencia_km

        print(f'patene: {patente_del_turno}, marca: {marca}, modelo: {modelo}, km: {km_del_turno}')

        id_service = obtener_service(modelo,marca,km_del_turno)
        service = Service.objects.get(id_service = id_service)
        print(f'id service: {id_service}')
        if id_service is None:
             return Response({'error': f'No existe un service para la marca "{marca}", modelo "{modelo}" para los {km_del_turno} km'}, status=status.HTTP_404_NOT_FOUND)

# -----------------------------------OBTENER GARANTIA TURNO-------------------------------------------------------------------------
        """url = f'https://autotech2.onrender.com/garantias/estado-garantia/{patente_del_turno}/'
        response = requests.get(url)
        print("llegue 1")
        print(response)
        if response.ok:
            data = response.text
            print(data)
            if data == "no_anulada":
                tiene_garantia = True
            else:
                tiene_garantia = False
        else:
            return print({'error':response.text, 'status':response.status_code})
        print("llegue 2") """
    
# -----------------------------------OBTENER COSTO TOTAL SERVICE--------------------------------------------------------------------
        id_tasks_reemplazadas = request.data.get('id_tasks_remplazadas')
        id_tasks_lista = json.loads(id_tasks_reemplazadas)

        print(f'partes a reemplazar {id_tasks_lista}')
        tiene_garantia = False
        costo_final_service = obtener_costo_final_service(tiene_garantia, id_service, id_tasks_lista)
# -----------------------------------OBTENER DURACION TOTAL SERVICE-----------------------------------------------------------------

        duracion_total_service = service.duracion_total
# ----------------------------------------------------------------------------------------------------------------------------------
        if Registro_service.objects.filter(id_turno=id_turno).exists():
            return Response({'error': 'El turno pasado ya existe en los registros'}, status=status.HTTP_400_BAD_REQUEST)

        turno_taller = Turno_taller.objects.get(pk=id_turno)
        print("llegue 3")
        registro_service = Registro_service.objects.create(id_turno = turno_taller
                                                              , id_service = service
                                                              , costo_total = costo_final_service
                                                              , duracion_total = duracion_total_service # pongo la del service, no de las tareas que solo se repararon
                                                              , garantia = tiene_garantia
                                                              , id_tasks_reemplazadas = id_tasks_reemplazadas)
        
        serializer = RegistroServiceSerializer(registro_service)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    








        """ try:
            validador.validar_diccionario(request)
        except ValidationError as e:
            error_messages = [str(error) for error in e.detail]
            return Response({'error': error_messages}, status=status.HTTP_400_BAD_REQUEST) """
        