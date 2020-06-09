# Generated by Django 3.0.7 on 2020-06-08 21:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cognome', models.CharField(max_length=100)),
                ('mail', models.CharField(max_length=100)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Corso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('prezzo', models.FloatField(default=0)),
                ('iscritti_max', models.IntegerField(default=0)),
                ('iscritti_attuali', models.IntegerField(default=0)),
                ('sedute_settimanali', models.IntegerField(default=0)),
                ('descrizione', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Iscrizione',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagato', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gym.Cliente')),
                ('corso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gym.Corso')),
            ],
            options={
                'unique_together': {('corso', 'cliente')},
            },
        ),
    ]
