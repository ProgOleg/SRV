# Generated by Django 2.1.3 on 2019-03-26 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0035_auto_20190326_2029"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="incoming",
            name="exchange_rates",
        ),
        migrations.AlterField(
            model_name="incoming",
            name="exchange_ratest",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="incoming_exchange_rates",
                to="srvbd.ExchangeRates",
            ),
        ),
    ]
