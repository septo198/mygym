# Generated by Django 3.0.7 on 2020-06-10 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iscrizione',
            name='mesi_durata',
            field=models.IntegerField(default=1),
        ),
    ]