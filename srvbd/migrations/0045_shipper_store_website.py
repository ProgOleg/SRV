# Generated by Django 2.1.3 on 2020-05-12 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0044_auto_20200506_2256"),
    ]

    operations = [
        migrations.AddField(
            model_name="shipper",
            name="store_website",
            field=models.CharField(default=None, max_length=100, null=True, verbose_name="Сайт магазина"),
        ),
    ]
