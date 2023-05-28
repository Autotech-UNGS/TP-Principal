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
        email
        """
        # datos que necesitamos
        taller_id = request.data.get("taller_id")
        email = request.data.get("email")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        duracion = 1
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        resultado_validacion = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='evaluacion', 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        
        # eliminamos el email del request
        datos = request.data.copy()
        del datos['email']
        datos['papeles_en_regla'] = False
        datos['tipo'] = 'evaluacion'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        datos['tecnico_id'] = None
        datos['frecuencia_km'] = None
        serializer = TurnoTallerSerializer(data=datos)
        
        # actualizamos el serializer, lo guardamos, y enviamos el email
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
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
        email
        """
        # datos que necesitamos
        taller_id = request.data.get("taller_id")
        email = request.data.get("email")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        duracion = 1
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        resultado_validacion = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='evaluacion', 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        
        # eliminamos el email del request
        datos = request.data.copy()
        del datos['email']
        datos['papeles_en_regla'] = True 
        datos['tipo'] = 'evaluacion'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        datos['tecnico_id'] = None
        datos['frecuencia_km'] = None
        serializer = TurnoTallerSerializer(data=datos)
        
        # actualizamos el serializer, lo guardamos, y enviamos el email
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
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
        email
        frecuencia_km
        marca
        modelo
        """
        # datos que necesitamos
        taller_id = request.data.get("taller_id")
        email = request.data.get("email")
        #email = obtener_email_usuario()
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        marca = request.data.get("marca")
        modelo = request.data.get("modelo")
        km = request.data.get("frecuencia_km")
        
        duracion = obtener_duracion_service(marca=marca, modelo=modelo, km=km)
        if duracion == -1:
            return HttpResponse("error: no existe un service con los datos especificados", status=400)
        
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        resultado_validacion = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='service', 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        if not validaciones.patente_registrada(patente):
            return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)
        if km == None:
            return HttpResponse("error: el service debe tener un kilometraje asociado", status=400)
        
        if km > 5000:
            if obtener_ultimo_service(patente) + 5000 != km:
                self.informar_perdida_de_garantia(patente)
        
        # eliminamos el email y los datos del service del request
        datos = request.data.copy()
        del datos['email']
        del datos['marca']
        del datos['modelo']
        datos['papeles_en_regla'] = True
        datos['tipo'] = 'service'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        datos['tecnico_id'] = None
        
        serializer = TurnoTallerSerializer(data=datos)
        # Actualizamos el serializer y enviamos un email
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
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
        # datos que necesitamos
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        origen = request.data.get("origen")
        
        duracion =  obtener_duracion_extraordinario(patente) if origen == 'extraordinario' else obtener_duracion_reparacion(patente)
        if duracion == -1:
            return HttpResponse("error: la patente no pertenece a la de un auto que ya haya sido evaluado en el taller.", status=400)
        
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        resultado_validacion = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='reparacion', 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        if origen == 'extraordinario':
            if not validaciones.patente_registrada(patente=patente):
                return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)               
        
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
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        duracion = 1
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        resultado_validacion = validaciones.validaciones_generales(taller_id=taller_id, patente=patente, tipo='extraordinario', 
                                                                   dia_inicio=dia_inicio_date, horario_inicio=horario_inicio_time,
                                                                   dia_fin= fecha_hora_fin[0], horario_fin=fecha_hora_fin[1])
        if resultado_validacion.status_code == 400:
            return resultado_validacion
        if not validaciones.patente_registrada(patente): 
            return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)
 
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