# Generated by Django 2.2.28 on 2022-07-26 21:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0055_auto_20220724_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='sparpart',
            name='image_link',
            field=models.TextField(null=True, verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='sparpart',
            name='part_num',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='sparpart',
            name='specification',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
    ]
