# Generated by Django 3.0.7 on 2020-06-11 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0008_auto_20200611_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='iscrizione',
            name='data_iscrizione',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='iscrizione',
            name='data_scadenza',
            field=models.DateField(default='1970-01-01'),
        ),
    ]
