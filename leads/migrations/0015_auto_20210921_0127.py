# Generated by Django 3.1.4 on 2021-09-21 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0014_imagenes_viajes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenes_viajes',
            name='imagen',
            field=models.ImageField(default='default.jpg', upload_to='imagenes-fletes/'),
        ),
    ]
