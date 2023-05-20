from django.http import JsonResponse, HttpResponse
from administracion.models import *
from rest_framework.response import Response
from .obtener_datos_usuario import *
from .validaciones_views import * 
from datetime import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EjecutarCron(ViewSet):
        @action(detail=False, methods=['get'])
        def ejecutar_cron(self, request):
                self.enviar_correo_prueba()
                self.modificar_estado_a_ausente()
                self.modificar_estado_a_terminado()
                return HttpResponse("cron ejecutado correctamente", status=200)
                
        # Cambia a 'ausente' el estado de los turnos que debían empezar hoy y no lo hicieron (su estado sigue siendo 'pendiente')
        def modificar_estado_a_ausente(self):
                hoy = date.today()
                turnos_del_dia = Turno_taller.objects.filter(fecha_inicio=hoy, estado='pendiente')
                for turno in turnos_del_dia:
                        turno.estado = 'ausente'
                        turno.save()
        
        # Cambia a 'terminado' el estado de los turnos que, al final del dia en que debían terminar, todavia tengan estado 'en_proceso'
        def modificar_estado_a_terminado(self):
                hoy = date.today()
                turnos_del_dia = Turno_taller.objects.filter(fecha_fin=hoy, estado='en_proceso')
                for turno in turnos_del_dia:
                        turno.estado = 'terminado'
                        turno.save()
        
        def enviar_correo_prueba(self):
                username = 'insomnia.autotech@gmail.com'
                password = 'tlrgdovrwrsacygp'
                mensaje = MIMEMultipart('alternative')
                mensaje['From'] = username
                mensaje['To'] = 'luciacsoria5@gmail.com'
                mensaje['Subject'] = 'CRON'
                hora = datetime.now()
                html = f""" <p> mensaje enviado a las {hora} con cron. Turnos modificados </p>"""
                parte_html = MIMEText(html, 'html')
                mensaje.attach(parte_html)
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
                        servidor.login(username, password)
                        servidor.send_message(mensaje)
