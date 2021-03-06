# Generated by Django 3.0.7 on 2020-06-12 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0009_auto_20200611_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Esercizio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_esercizio', models.CharField(max_length=100)),
                ('ripetizioni', models.IntegerField(default=0)),
                ('serie', models.IntegerField(default=1)),
                ('recupero', models.IntegerField(default=30)),
                ('scheda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gym.Scheda')),
            ],
        ),
    ]
