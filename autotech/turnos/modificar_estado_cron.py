from administracion.models import Turno_taller
from datetime import date
"""
1) Ejecuta el siguiente comando para generar el archivo cron y configurar la tarea programada:
        python manage.py crontab add
2) Reinicia el servicio de cron para asegurarte de que los cambios se apliquen:
        sudo service cron restart
"""

# Cambia a 'cancelado' el estado de los turnos que al final del dia todavia tengan estado 'pendiente'
def modificar_estado():
    hoy = date.today()
    turnos_del_dia = Turno_taller.objects.filter(fecha_inicio=hoy, estado='pediente')
    for turno in turnos_del_dia:
        turno.estado = 'cancelado'
        turno.save()
        print('Estado del turno modificado')