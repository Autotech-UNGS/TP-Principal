from django.http import JsonResponse, HttpResponse
from administracion.models import *
from administracion.serializers import TurnoTallerSerializer
from rest_framework.response import Response
from .enviar_turno_email import EnvioDeEmail
from .obtener_datos_usuario import *
from .validaciones_views import * 
from datetime import *

class CrearActualizarTurnosViewSet(ViewSet):
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
        #DURACION
        # validaciones:
        taller_valido = self.validar_taller(request=request)
        if taller_valido.status_code == 400:
            return taller_valido
        dias_horarios_validos = self.validar_dias_horarios(request=request)
        if dias_horarios_validos.status_code == 400:
            return dias_horarios_validos
        
        # datos que necesitamos para el envío del email
        taller_id = request.data.get("taller_id")
        email = request.data.get("email")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # eliminamos el email del request
        datos = request.data.copy()
        del datos['email']
        serializer = TurnoTallerSerializer(data=datos)
        
        if serializer.is_valid():
            serializer.validated_data['papeles_en_regla'] = False 
            serializer.validated_data['tipo'] = 'evaluacion'
            serializer.validated_data['estado'] = 'pendiente'
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            EnvioDeEmail.enviar_correo('evaluacion', email, dia_inicio_date, horario_inicio_time, direccion_taller, patente)
        return Response(serializer.data)
        
        
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
        #DURACION
        # validaciones:
        taller_valido = self.validar_taller(request=request)
        if taller_valido.status_code == 400:
            return taller_valido
        dias_horarios_validos = self.validar_dias_horarios(request=request)
        if dias_horarios_validos.status_code == 400:
            return dias_horarios_validos
        
        # datos que necesitamos para el envío del email
        taller_id = request.data.get("taller_id")
        email = request.data.get("email")
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # eliminamos el email del request
        datos = request.data.copy()
        del datos['email']
        serializer = TurnoTallerSerializer(data=datos)
        
        if serializer.is_valid():
            serializer.validated_data['papeles_en_regla'] = True 
            serializer.validated_data['tipo'] = 'evaluacion'
            serializer.validated_data['estado'] = 'pendiente'
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            EnvioDeEmail.enviar_correo('evaluacion', email, dia_inicio_date, horario_inicio_time, direccion_taller, patente)
        return Response(serializer.data)
        
        
    @action(detail=False, methods=['post'])
    def crear_turno_service(self, request):
        """
        taller_id
        patente
        fecha_inicio
        hora_inicio
        frecuencia_km
        """
        #DURACION
        # validaciones:
        if not patente_registrada(patente): # necesitamos un endpoint que nos de todas las patentes de vehículos
            return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)
        if request.data.get("frecuencia_km") == None:
            return HttpResponse("error: el service debe tener un kilometraje asociado", status=400)
        taller_valido = self.validar_taller(request=request)
        if taller_valido.status_code == 400:
            return taller_valido
        dias_horarios_validos = self.validar_dias_horarios(request=request)
        if dias_horarios_validos.status_code == 400:
            return dias_horarios_validos
        
        # datos que necesitamos para el envío del email
        taller_id = request.data.get("taller_id")
        email = obtener_email_usuario()
        patente = request.data.get("patente")
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        
        # eliminamos el email del request
        datos = request.data.copy()
        del datos['email']
        serializer = TurnoTallerSerializer(data=datos)
        
        if serializer.is_valid():
            serializer.validated_data['papeles_en_regla'] = True 
            serializer.validated_data['tipo'] = 'service'
            serializer.validated_data['estado'] = 'pendiente'
            serializer.save()
            direccion_taller = obtener_direccion_taller(taller_id)
            EnvioDeEmail.enviar_correo('service', email, dia_inicio_date, horario_inicio_time, direccion_taller, patente)
        return Response(serializer.data)
        
        
    @action(detail=False, methods=['post'])
    def crear_turno_reparacion(self, request):
        """
        taller_id
        patente
        fecha_inicio
        hora_inicio
        """
        #DURACION
        # validaciones:
        if not existe_turno_evaluacion(request.data.get('patente')):
            return HttpResponse("error: la patente no pertenece a la de un auto evaluado en el taller.", status=400)
        taller_valido = self.validar_taller(request=request)
        if taller_valido.status_code == 400:
            return taller_valido
        dias_horarios_validos = self.validar_dias_horarios(request=request)
        if dias_horarios_validos.status_code == 400:
            return dias_horarios_validos
        
        serializer = TurnoTallerSerializer(data=request)
        if serializer.is_valid():
            serializer.validated_data['papeles_en_regla'] = True 
            serializer.validated_data['tipo'] = 'reparacion'
            serializer.validated_data['estado'] = 'pendiente'
            serializer.save()
        return Response(serializer.data)
        
        
    @action(detail=False, methods=['post'])
    def crear_turno_extraordinario(self, request):
        """
        taller_id
        patente
        fecha_inicio
        hora_inicio
        fecha_fin
        hora_fin
        """
        #DURACION?
        # validaciones:
        if not patente_registrada(request.data.get('patente')): # necesitamos un endpoint que nos de todas las patentes de vehículos
            return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)
        taller_valido = self.validar_taller(request=request)
        if taller_valido.status_code == 400:
            return taller_valido
        dias_horarios_validos = self.validar_dias_horarios(request=request)
        if dias_horarios_validos.status_code == 400:
            return dias_horarios_validos
        
        serializer = TurnoTallerSerializer(data=request)
        if serializer.is_valid():
            serializer.validated_data['papeles_en_regla'] = True 
            serializer.validated_data['tipo'] = 'extraordinario'
            serializer.validated_data['estado'] = 'pendiente'
            serializer.save()
        return Response(serializer.data)        
        

    def validar_taller(self, request) -> HttpResponse:
        taller_id = request.data.get("taller_id")
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        horario_fin_time = datetime.strptime(request.data.get("hora_fin"), '%H:%M:%S').time()
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        dia_fin_date = datetime.strptime(request.data.get("fecha_fin"), '%Y-%m-%d').date()
        
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)
        if not taller_esta_disponible(taller_id, dia_inicio_date, horario_inicio_time, dia_fin_date , horario_fin_time):
            return HttpResponse("error: ese dia no esta disponible en ese horario", status=400)
        return HttpResponse("Taller correcto", status=200)
        
    def validar_dias_horarios(self, request) -> HttpResponse:
        horario_inicio_time = datetime.strptime(request.data.get("hora_inicio"), '%H:%M:%S').time()
        horario_fin_time = datetime.strptime(request.data.get("hora_fin"), '%H:%M:%S').time()
        dia_inicio_date = datetime.strptime(request.data.get("fecha_inicio"), '%Y-%m-%d').date()
        dia_fin_date = datetime.strptime(request.data.get("fecha_fin"), '%Y-%m-%d').date()
        
        if not horarios_exactos(horario_inicio_time, horario_fin_time):
            return HttpResponse("error: los horarios de comienzo y fin de un turno deben ser horas exactas", status=400)
        if not horarios_dentro_de_rango(dia_inicio_date, horario_inicio_time, horario_fin_time):
            return HttpResponse("error: los horarios superan el limite de la jornada laboral", status=400)
        if not dia_valido(dia_inicio_date):
            return HttpResponse("error: no se puede sacar un turno para una fecha que ya paso.", status=400)
        if not dia_hora_coherentes(dia_inicio_date, horario_inicio_time, dia_fin_date, horario_fin_time):
            return HttpResponse("error: un turno no puede terminar antes de que empiece", status=400)
        return HttpResponse("Dias horarios correctos", status=200)
        
    """
    # esta vista es para:
        # para cuando el cliente saca un turno en la página --> saca para service y para evaluación
    @action(detail=False, methods=['post'])
    def crearTurno(self, request):
        dia = request.data.get("fecha_inicio")
        dia_fin = request.data.get("fecha_fin")
        horario_inicio = request.data.get("hora_inicio")
        horario_fin = request.data.get("hora_fin")
        taller_id = request.data.get("taller_id")
        tipo = request.data.get("tipo")
        km = request.data.get("frecuencia_km")
        patente = request.data.get("patente")

        horario_inicio_time = datetime.strptime(horario_inicio, '%H:%M:%S').time()
        horario_fin_time = datetime.strptime(horario_fin, '%H:%M:%S').time()
        dia_inicio_date = datetime.strptime(dia, '%Y-%m-%d').date()
        dia_fin_date = datetime.strptime(dia_fin, '%Y-%m-%d').date()

        if tipo == 'reparacion' and not existe_turno_evaluacion(patente):
            return HttpResponse("error: la patente no pertenece a la de un auto evaluado en el taller.", status=400)
        if (tipo == 'service' or tipo == 'extraordinario') and not patente_registrada(patente): # necesitamos un endpoint que nos de todas las patentes de vehículos
            return HttpResponse("error: la patente no está registrada como perteneciente a un cliente", status=400)
        if tipo == "service" and km == None:
            return HttpResponse("error: el service debe tener un kilometraje asociado", status=400)
        if not existe_taller(taller_id):
            return HttpResponse("error: el id ingresado no pertenece a ningún taller en el sistema", status=400)
        if not horarios_exactos(horario_inicio_time, horario_fin_time):
            return HttpResponse("error: los horarios de comienzo y fin de un turno deben ser horas exactas", status=400)
        if not horarios_dentro_de_rango(dia_inicio_date, horario_inicio_time, horario_fin_time):
            return HttpResponse("error: los horarios superan el limite de la jornada laboral", status=400)
        if not dia_valido(dia_inicio_date):
            return HttpResponse("error: no se puede sacar un turno para una fecha que ya paso.", status=400)
        if not dia_hora_coherentes(dia_inicio_date, horario_inicio_time, dia_fin_date, horario_fin_time):
            return HttpResponse("error: un turno no puede terminar antes de que empiece", status=400)
        if not taller_esta_disponible(taller_id, dia_inicio_date, horario_inicio_time, dia_fin_date , horario_fin_time):
            return HttpResponse("error: ese dia no esta disponible en ese horario", status=400)
        
        serializer=TurnoTallerSerializer(data=request.data)
        if serializer.is_valid():
            if tipo == 'evaluacion':
                 serializer.validated_data['papeles_en_regla'] = False
            serializer.save()
            if tipo == 'evaluacion' or tipo == 'service':   
                #email_usuario = request.META.get('email') # obtenemos 'email' del header. Otra opcion es request.headers.get('NombreEncabezado')
                email_usuario = obtener_email_usuario()
                direccion_taller = obtener_direccion_taller(taller_id)
                EnvioDeEmail.enviar_correo(tipo, email_usuario, dia_inicio_date, horario_inicio_time, direccion_taller)
        return Response(serializer.data)
    """
    
    
    @action(detail=True, methods=['post'])
    def turnoUpdate(self, request, id_turno):
        try:
            turno=Turno_taller.objects.get(id_turno=id_turno)
        except:
            return HttpResponse("error: el id ingresado no pertenece a ningún turno en el sistema", status=400)
        else:
            serializer=TurnoTallerSerializer(instance=turno,data=request.data)
            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data)