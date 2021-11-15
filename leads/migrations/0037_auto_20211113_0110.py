# Generated by Django 3.1.4 on 2021-11-13 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0036_auto_20211113_0105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordinates',
            name='id',
        ),
        migrations.AddField(
            model_name='coordinates',
            name='viaje',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='leads.viajes'),
            preserve_default=False,
        ),
    ]