# Generated by Django 3.1.4 on 2021-09-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0012_viajes_cantidad_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='viajes',
            name='status',
            field=models.CharField(default='En ruta', max_length=30),
        ),
    ]
