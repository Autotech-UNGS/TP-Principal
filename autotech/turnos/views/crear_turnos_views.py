from django.http import JsonResponse, HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from ..enviar_turno_email import EnvioDeEmail
from ..obtener_datos import *
from datetime import *
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from reparaciones.views import RegistroReparacionViewSet
from ..validaciones_crear_turno import validaciones
from ..garantias import GestionGarantias

class CrearActualizarTurnosViewSet(ViewSet):

# ------------------------------------------------------------------------------------------------ #
# ------------------------------------- turno evaluacion: web ------------------------------------ #
# ------------------------------------------------------------------------------------------------ #

    # papeles en regla == False        
    @action(detail=False, methods=['post'])
    def crear_turno_evaluacion_web(self, request):
        """
        taller_id
        patente
        fecha_inicio
        hora_inicio
        """
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # duracion y fecha/hora fin:
        duracion = 1
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        # validaciones:
        resultado_validacion = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='evaluacion', 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        
        datos = request.data.copy()
        datos['papeles_en_regla'] = False
        datos['tipo'] = 'evaluacion'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        datos['tecnico_id'] = None
        datos['frecuencia_km'] = None
        serializer = TurnoTallerSerializer(data=datos)
        
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            email = obtener_email_usuario(patente)
            if email:
                EnvioDeEmail.enviar_correo('evaluacion', email, dia_inicio_date, horario_inicio_time, direccion_taller, patente)
            return Response(serializer.data)        
        else:
            return HttpResponse("error: request inválido", status=400)
        
# ------------------------------------------------------------------------------------------------ #
# ---------------------------------- turno evaluacion: presencial -------------------------------- #
# ------------------------------------------------------------------------------------------------ #        
        
    # papeles en regla == True
    @action(detail=False, methods=['post'])
    def crear_turno_evaluacion_presencial(self, request):
        """
        taller_id
        patente
        fecha_inicio
        hora_inicio
        """
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # duracion y fecha/hora fin:
        duracion = 1
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        # validaciones:
        resultado_validacion = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='evaluacion', 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        
        datos = request.data.copy()
        datos['papeles_en_regla'] = True 
        datos['tipo'] = 'evaluacion'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        datos['tecnico_id'] = None
        datos['frecuencia_km'] = None
        serializer = TurnoTallerSerializer(data=datos)
        
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            email = obtener_email_usuario(patente)
            if email:
                EnvioDeEmail.enviar_correo('evaluacion', email, dia_inicio_date, horario_inicio_time, direccion_taller, patente)
            return Response(serializer.data)        
        else:
            return HttpResponse("error: request inválido", status=400)
        
# ------------------------------------------------------------------------------------------------ #
# ---------------------------------------- turno service ----------------------------------------- #
# ------------------------------------------------------------------------------------------------ #
        
    @action(detail=False, methods=['post'])
    def crear_turno_service(self, request):
        """
        taller_id
        patente
        fecha_inicio
        hora_inicio
        frecuencia_km
        """
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        km = request.data.get("frecuencia_km")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # frecuencias de services, duracion y fecha/hora fin:
        if not validaciones.patente_registrada(patente=patente):
            return HttpResponse(f"error: la patente no está registrada como perteneciente a un cliente: {patente}", status=400)
        
        frecuencia_service_solicitado = obtener_frecuencia_service_solicitado(patente, km)
        frecuencia_ultimo_service = obtener_frecuencia_ultimo_service(patente) 
        duracion = obtener_duracion_service_vehiculo(patente, km=frecuencia_service_solicitado)
        if duracion == 0:
            return HttpResponse("error: no existe un service con los datos especificados", status=400)
        
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        # validaciones:
        resultado_validacion = validaciones.validaciones_service(taller_id=taller_id, patente=patente, 
                                                                 dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                 dia_fin=fecha_hora_fin[0], horario_fin=fecha_hora_fin[1],
                                                                 km=km, frecuencia_ultimo_service=frecuencia_ultimo_service, 
                                                                 frecuencia_service_solicitado=frecuencia_service_solicitado)          
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        
        # garantia
        garantia_vigente = GestionGarantias.garantia_vigente(patente=patente, fecha_turno=dia_inicio_date, ultimo_service=frecuencia_ultimo_service, service_actual=frecuencia_service_solicitado)
        if not garantia_vigente:
            GestionGarantias.informar_perdida_garantia(patente)
                # informar que se debe cobrar el service
        
        datos = request.data.copy()
        datos['papeles_en_regla'] = True
        datos['tipo'] = 'service'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        datos['tecnico_id'] = None
        datos['frecuencia_km'] = str(frecuencia_service_solicitado)
        
        serializer = TurnoTallerSerializer(data=datos)
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            email = obtener_email_usuario(patente)
            if email:
                EnvioDeEmail.enviar_correo('service', email, dia_inicio_date, horario_inicio_time, direccion_taller, patente)
            return Response(serializer.data)        
        else:
            return HttpResponse("error: request inválido", status=400)
        
# ------------------------------------------------------------------------------------------------ #
# --------------------------------------- turno reparacion --------------------------------------- #
# ------------------------------------------------------------------------------------------------ #        
        
    @action(detail=False, methods=['post'])
    def crear_turno_reparacion(self, request):
        """
        taller_id
        patente
        fecha_inicio
        hora_inicio
        origen
        """
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        origen = request.data.get("origen")
        
        # duracion y fecha/hora fin:
        duracion =  obtener_duracion_extraordinario(patente) if origen == 'extraordinario' else obtener_duracion_reparacion(patente)
        if duracion == 0:
            return HttpResponse("error: la patente no pertenece a la de un auto que ya haya sido evaluado en el taller.", status=400)
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        # validaciones:
        resultado_validacion = validaciones.validaciones_reparacion(taller_id=taller_id, patente=patente, 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1],
                                                                   origen=origen)
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        
        datos = request.data.copy()
        del datos['origen']
        datos['papeles_en_regla'] = True
        datos['tipo'] = 'reparacion'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        
        serializer = TurnoTallerSerializer(data=datos)
        if serializer.is_valid():
            turno = serializer.save()
            registro_reparacion = RegistroReparacionViewSet()
            registro_reparacion.registrar(turno, origen)
            return Response(serializer.data)             
        else:
            return HttpResponse("error: request inválido", status=400)
        
# ------------------------------------------------------------------------------------------------ #
# ------------------------------------- turno extraordinario ------------------------------------- #
# ------------------------------------------------------------------------------------------------ #        
        
    @action(detail=False, methods=['post'])
    def crear_turno_extraordinario(self, request):
        """
        taller_id
        patente
        fecha_inicio
        hora_inicio
        """
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # duracion y fecha/hora fin:
        duracion = 1
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        # validaciones:
        resultado_validacion = validaciones.validaciones_extraordinario(taller_id=taller_id, patente=patente, 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
 
        datos = request.data.copy()
        datos['papeles_en_regla'] = True 
        datos['tipo'] = 'extraordinario'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        datos['tecnico_id'] = None
        datos['frecuencia_km'] = None
        
        serializer = TurnoTallerSerializer(data=datos)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)        
        else:
            return HttpResponse("error: request inválido", status=400)
    
    def informar_perdida_de_garantia(self, patente:str):
        return True

# ------------------------------------------------------------------------------------------------ #
# --------------------------------------- actualizar turno --------------------------------------- #
# ------------------------------------------------------------------------------------------------ #

    @action(detail=False, methods=['post'])
    def turnoUpdate(self, request, id_turno):    
        turno= Turno_taller.objects.get(id_turno=id_turno)
        serializer=TurnoTallerSerializer(instance=turno,data=request.data)
        if serializer.is_valid():
            serializer.save()
    
        return Response(serializer.data)