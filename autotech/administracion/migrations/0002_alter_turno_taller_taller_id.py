# Generated by Django 4.2.1 on 2023-05-13 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno_taller',
            name='taller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.taller'),
        ),
    ]
