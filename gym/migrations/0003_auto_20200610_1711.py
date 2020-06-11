# Generated by Django 3.0.7 on 2020-06-10 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0002_iscrizione_mesi_durata'),
    ]

    operations = [
        migrations.AddField(
            model_name='corso',
            name='posti_rimanenti',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='iscrizione',
            name='costo_complessivo',
            field=models.FloatField(default=0),
        ),
    ]
