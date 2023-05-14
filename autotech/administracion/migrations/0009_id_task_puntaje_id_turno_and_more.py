# Generated by Django 4.2.1 on 2023-05-14 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0008_remove_registro_evaluacion_id_tasks_realizadas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='id_task_puntaje',
            name='id_turno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='administracion.turno_taller'),
        ),
        migrations.AlterField(
            model_name='id_task_puntaje',
            name='id_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.checklist_evaluacion'),
        ),
    ]
