# Generated by Django 2.1.3 on 2019-03-23 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0031_auto_20190324_0103"),
    ]

    operations = [
        migrations.AddField(
            model_name="incoming",
            name="exchange_rates",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
    ]
