# Generated by Django 3.0.7 on 2020-06-12 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0016_auto_20200612_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prenotazione',
            name='end_time',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='prenotazione',
            name='start_time',
            field=models.CharField(default='', max_length=20),
        ),
    ]
