# Generated by Django 3.1.4 on 2021-09-15 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0009_auto_20210907_1326'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Lead',
            new_name='Viajes',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]