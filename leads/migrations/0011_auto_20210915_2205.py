# Generated by Django 3.1.4 on 2021-09-15 22:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0010_auto_20210915_2133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='viajes',
            old_name='age',
            new_name='cantidad',
        ),
        migrations.RenameField(
            model_name='viajes',
            old_name='first_name',
            new_name='destino',
        ),
        migrations.RenameField(
            model_name='viajes',
            old_name='last_name',
            new_name='mercancia',
        ),
        migrations.AddField(
            model_name='viajes',
            name='f_llegada',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='viajes',
            name='f_salida',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='viajes',
            name='origen',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='viajes',
            name='tipo_embarque',
            field=models.CharField(choices=[('Caja Seca', 'Caja Seca'), ('Tolva', 'Tolva'), ('Refrigerado', 'Refrigerado')], default=None, max_length=30),
        ),
    ]
