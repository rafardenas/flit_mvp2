# Generated by Django 3.1.4 on 2021-09-28 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0022_imagenes_viajes_added_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenes_viajes',
            name='added_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
