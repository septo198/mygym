# Generated by Django 3.0.7 on 2020-06-10 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0004_auto_20200610_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iscrizione',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
