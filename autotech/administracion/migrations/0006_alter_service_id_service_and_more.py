# Generated by Django 4.2.1 on 2023-05-26 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_checklist_service_service_tasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='id_service',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='service_tasks',
            name='id_id_tasks',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
    ]