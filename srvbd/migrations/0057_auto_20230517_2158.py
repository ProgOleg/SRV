# Generated by Django 2.2.28 on 2023-05-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0056_auto_20220727_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparpart',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Наименование'),
        ),
    ]
