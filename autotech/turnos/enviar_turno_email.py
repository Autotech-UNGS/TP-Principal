import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, time

class EnvioDeEmail:
    username = 'sorialuciac5@gmail.com'
    password = 'isymznzitbnuycra'
    url = 'https://www.google.com/'  
    
    @classmethod
    def enviar_correo(cls, tipo_turno:str, destinatario: str, fecha_inicio: date, hora_inicio: time, direccion_taller: str):
        mensaje = MIMEMultipart('alternative')
        mensaje['From'] = cls.username
        mensaje['To'] = destinatario
        mensaje['Subject'] = 'Recordatorio: turno KarU'
        
        if tipo_turno == 'evaluacion':
            html = cls.generar_mensaje_evaluacion(destinatario, fecha_inicio, hora_inicio, direccion_taller)
        elif tipo_turno == 'service':
            html = cls.generar_mensaje_service(destinatario, fecha_inicio, hora_inicio, direccion_taller)
            
        parte_html = MIMEText(html, 'html')
        mensaje.attach(parte_html)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(cls.username, cls.password)
            servidor.send_message(mensaje)

    @classmethod
    def generar_mensaje_evaluacion(cls, destinatario: str, fecha_inicio:date, hora_inicio:time, direccion_taller: str):
        html = f"""
        <html>
        <body>
            <h1> Buenos días, {destinatario} </h1>
            <p> Solicitaste un turno con KarU para vender un vehículo, para el día {fecha_inicio} a las {hora_inicio} </p>
            <p> Te esperamos ese día en nuestro taller en {direccion_taller} </p>
            <p> Recordá venir con treinta minutos de anticipación, y traer toda la documentación correspondiente, incluyendo la cedula verde del vehículo </p>
            <br>
            <p> Que tengas un buen dia! </p>
            <p> Equipo de KarU.</p>
            <a href='{cls.url}'> KarU </a>

        </body>
        </html>
        """
        return html
    
    @classmethod
    def generar_mensaje_service(cls, destinatario: str, fecha_inicio:date, hora_inicio:time, direccion_taller: str):
        html = f"""
        <html>
        <body>
            <h1> Buenos días, {destinatario} </h1>
            <p> Solicitaste un turno con KarU para realizarle un service a tu vehículo, para el día {fecha_inicio} a las {hora_inicio} </p>
            <p> Te esperamos ese día en nuestro taller en {direccion_taller} </p>
            <p> El día del turno, evaluaremos el estado de tu garantía. Recordá que la garantía deja de ser válida si no realizaste el último service en alguno de nuestros talleres </p>
            <br>
            <p> Que tengas un buen dia! </p>
            <p> Equipo de KarU.</p>
            <a href={cls.url}> KarU </a>

        </body>
        </html>
        """
        return html