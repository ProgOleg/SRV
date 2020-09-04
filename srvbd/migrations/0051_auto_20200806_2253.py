# Generated by Django 2.1.3 on 2020-08-06 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0050_auto_20200708_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.CharField(choices=[('MA', 'Мастер'), ('CL', 'Клиент'), ('OW', 'Собственник')], default='CL', max_length=2),
        ),
    ]
