import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, time

class EnvioDeEmail:
    username = 'insomnia.autotech@gmail.com'
    password = 'tlrgdovrwrsacygp'
    url = 'https://karu-web-back.onrender.com/'  
    
    @classmethod
    def enviar_correo(cls, tipo_turno:str, destinatario: str, nombre:str, fecha_inicio: date, hora_inicio: time, direccion_taller: str, patente: str, duracion: int, costo:float):
        mensaje = MIMEMultipart('alternative')
        mensaje['From'] = cls.username
        mensaje['To'] = destinatario
        mensaje['Subject'] = 'Recordatorio: turno KarU'
        
        if tipo_turno == 'evaluacion':
            html = cls.generar_mensaje_evaluacion(nombre, fecha_inicio, hora_inicio, direccion_taller, patente)
        elif tipo_turno == 'service':
            html = cls.generar_mensaje_service(nombre, fecha_inicio, hora_inicio, direccion_taller, patente, duracion, costo)
            
        parte_html = MIMEText(html, 'html')
        mensaje.attach(parte_html)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(cls.username, cls.password)
            servidor.send_message(mensaje)

    @classmethod
    def generar_mensaje_evaluacion(cls, nombre:str, fecha_inicio:date, hora_inicio:time, direccion_taller: str, patente: str):
        html = f"""
        <html>
        <body>
            <h1> ¡Mucho gusto, {nombre}! </h1>
            <p> Solicitaste un turno con KarU para que evaluemos tu vehículo con patente {patente}, el día {fecha_inicio} a las {hora_inicio}hs. </p>
            <p> Te esperamos ese día en nuestro taller en {direccion_taller} La evaluación durará aproximadamente una hora, y no tendrá costo. </p>
            <p> Recorda traer tu cédula verde, y , si tu documentación aún no fue aprobada, recordá venir con treinta minutos de anticipación, y traer toda la documentación correspondiente. </p>
            <br>
            <p> ¡Que tengas un buen dia! </p>
            <p> Equipo de KarU.</p>
            <a href='{cls.url}'> KarU </a>

        </body>
        </html>
        """
        return html
    
    @classmethod
    def generar_mensaje_service(cls, nombre:str, fecha_inicio:date, hora_inicio:time, direccion_taller: str, patente: str, duracion: int, costo:float):
        html = f"""
        <html>
        <body>
            <h1> ¡Hola de nuevo, {nombre}! </h1>
            <p> Solicitaste un turno con KarU para realizarle un service a tu vehículo con patente {patente}, para el día {fecha_inicio} a las {hora_inicio}hs. </p>
            <p> Te esperamos ese día en nuestro taller en {direccion_taller} El service durará aproximadamente {duracion} horas, y su costo será de hasta ${costo}.</p>
            <p> Recorda traer tu cédula verde.</p>
            
            <br>
            <p> ¡Que tengas un buen dia! </p>
            <p> Equipo de KarU.</p>
            <a href={cls.url}> KarU </a>

        </body>
        </html>
        """
        return html