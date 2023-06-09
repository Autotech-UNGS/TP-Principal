from django.http import JsonResponse, HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from ..enviar_turno_email import EnvioDeEmail
from ..obtener_datos import *
from datetime import *
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from reparaciones.views import RegistroReparacionViewSet
from ..validaciones_crear_turno import validaciones
from garantias.gestion_garantia import GestionGarantias

class CrearActualizarTurnosViewSet(ViewSet):

# ------------------------------------------------------------------------------------------------ #
# ------------------------------------- turno evaluacion: web ------------------------------------ #
# ------------------------------------------------------------------------------------------------ #

    # papeles en regla == False        
    @action(detail=False, methods=['post'])
    def crear_turno_evaluacion_web(self, request):
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        patente = patente.upper()
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # duracion y fecha/hora fin:
        duracion = 1
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        # validaciones:
        resultado_validacion = validaciones.validaciones_evaluacion(taller_id=taller_id, patente=patente, 
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
        datos['patente'] = patente
        serializer = TurnoTallerSerializer(data=datos)
        
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            email = obtener_email_usuario(patente)
            nombre = obtener_nombre_usuario(patente)
            if email:
                EnvioDeEmail.enviar_correo('evaluacion', email, nombre, dia_inicio_date, horario_inicio_time, direccion_taller, patente, 0, 0)
                print("email enviado a: ", email)
            return Response(serializer.data)        
        else:
            return HttpResponse("error: request inválido", status=400)
        
# ------------------------------------------------------------------------------------------------ #
# ---------------------------------- turno evaluacion: presencial -------------------------------- #
# ------------------------------------------------------------------------------------------------ #        
        
    # papeles en regla == True
    @action(detail=False, methods=['post'])
    def crear_turno_evaluacion_presencial(self, request):   
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        patente = patente.upper()
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # duracion y fecha/hora fin:
        duracion = 1
        fecha_hora_fin = obtener_fecha_hora_fin(dia_inicio_date, horario_inicio_time, duracion)
        
        # validaciones:
        resultado_validacion = validaciones.validaciones_evaluacion(taller_id=taller_id, patente=patente, 
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
        datos['patente'] = patente
        serializer = TurnoTallerSerializer(data=datos)
        
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            email = obtener_email_usuario(patente)
            nombre = obtener_nombre_usuario(patente)
            if email:
                EnvioDeEmail.enviar_correo('evaluacion', email, nombre, dia_inicio_date, horario_inicio_time, direccion_taller, patente, 0, 0)
                print("email enviado a: ", email)
            return Response(serializer.data)        
        else:
            return HttpResponse("error: request inválido", status=400)
        
# ------------------------------------------------------------------------------------------------ #
# ---------------------------------------- turno service ----------------------------------------- #
# ------------------------------------------------------------------------------------------------ #
        
    @action(detail=False, methods=['post'])
    def crear_turno_service(self, request):   
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        patente = patente.upper()
        km = request.data.get("frecuencia_km")
        if not validaciones.patente_registrada(patente=patente):
            return HttpResponse(f"error: la patente no está registrada como perteneciente a un cliente: {patente}", status=400)
        if km == None:
            return HttpResponse("error: el service debe tener un kilometraje asociado", status=400)
        
        km = redondear_a_multiplo_de_cincomil(km)
        
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # frecuencias de services, duracion y fecha/hora fin:
        frecuencia_service_solicitado = obtener_frecuencia_service_solicitado(patente, km)
        frecuencia_ultimo_service = obtener_frecuencia_ultimo_service(patente) 
        
        duracion = obtener_duracion_service_vehiculo(patente, km_solicitado=frecuencia_service_solicitado)

        if km <= obtener_km_de_venta(patente=patente):
                return HttpResponse(f"error: el service ingresado no es valido: se solicita un service de {km}km para un vehiculo vendido con {obtener_km_de_venta(patente)}km", status=400)            
        if frecuencia_ultimo_service != 0 and frecuencia_ultimo_service >= frecuencia_service_solicitado:
                return HttpResponse(f"error: el service ingresado ya se había realizado antes: service de {frecuencia_ultimo_service}, {patente}", status=400)
        if duracion == 0:
            return HttpResponse(f"error: no existe un service con los datos especificados: {frecuencia_service_solicitado}", status=400)
        
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
        try:
            garantia_vigente = GestionGarantias.garantia_seguiria_vigente(patente=patente, fecha_turno=dia_inicio_date, ultimo_service=frecuencia_ultimo_service, service_solicitado=frecuencia_service_solicitado)
            print("seguiria vigente: ", garantia_vigente)
            if not garantia_vigente:
                GestionGarantias.informar_perdida_garantia(patente)
                print("llegue al costo")
                costo = obtener_costo_base_service_vehiculo(patente=patente, km_solicitado=frecuencia_service_solicitado) + obtener_costo_total_service_vehiculo(patente=patente, km_solicitado=frecuencia_service_solicitado)
                print("pase el costo")
            else:
                costo = obtener_costo_base_service_vehiculo(patente=patente, km_solicitado=frecuencia_service_solicitado)
        except Exception as e:
            print(e)
            return HttpResponse(f"error: El vehiculo con la patente ingresada no fue vendido o no se le ha creado una factura: {patente}", status=400)
        
        
        datos = request.data.copy()
        datos['papeles_en_regla'] = True
        datos['tipo'] = 'service'
        datos['estado'] = 'pendiente'
        datos['fecha_fin'] = fecha_hora_fin[0].strftime("%Y-%m-%d")
        datos['hora_fin'] = fecha_hora_fin[1].strftime("%H:%M:%S")
        datos['tecnico_id'] = None
        datos['frecuencia_km'] = str(frecuencia_service_solicitado)
        datos['patente'] = patente
        
        serializer = TurnoTallerSerializer(data=datos)
        if serializer.is_valid():
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            email = obtener_email_usuario(patente)
            nombre = obtener_nombre_usuario(patente)
            if email:
                EnvioDeEmail.enviar_correo('service', email, nombre, dia_inicio_date, horario_inicio_time, direccion_taller, patente, duracion, costo)
                print("email enviado a: ", email)
            return Response(serializer.data)        
        else:
            return HttpResponse("error: request inválido", status=400)
        
# ------------------------------------------------------------------------------------------------ #
# --------------------------------------- turno reparacion --------------------------------------- #
# ------------------------------------------------------------------------------------------------ #        
        
    @action(detail=False, methods=['post'])
    def crear_turno_reparacion(self, request): 
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        patente = patente.upper()
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        origen = request.data.get("origen")
        
        duracion =  obtener_duracion_extraordinario(patente) if origen == 'extraordinario' else obtener_duracion_reparacion(patente)
    
        if duracion == -1:
           return HttpResponse(f'La patente {patente} pertenece a un vehiculo que ha sido evaluado y no necesita reparaciones.', status=400)
        # duracion y fecha/hora fin:
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
        datos['patente'] = patente
        
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
        # datos:
        taller_id = request.data.get("taller_id")
        patente = request.data.get("patente")
        patente = patente.upper()
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
        datos['patente'] = patente
        
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