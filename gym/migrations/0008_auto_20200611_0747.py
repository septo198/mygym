# Generated by Django 3.0.7 on 2020-06-11 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0007_auto_20200611_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corso',
            name='foto',
            field=models.ImageField(default='placeholder.png', upload_to=''),
        ),
    ]