# Generated by Django 3.1.4 on 2021-10-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0032_auto_20211001_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viajes',
            name='destino',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='viajes',
            name='origen',
            field=models.CharField(max_length=70),
        ),
    ]