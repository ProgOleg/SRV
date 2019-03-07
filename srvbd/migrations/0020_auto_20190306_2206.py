# Generated by Django 2.1.3 on 2019-03-06 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0019_auto_20190221_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='mod',
            field=models.CharField(max_length=50, unique=True, verbose_name='Модель:'),
        ),
        migrations.AlterField(
            model_name='device',
            name='pnc',
            field=models.CharField(blank=True, max_length=50, verbose_name='PNC-код:'),
        ),
        migrations.AlterField(
            model_name='device',
            name='serial_number',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Серийный номер:'),
        ),
    ]
