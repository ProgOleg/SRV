# Generated by Django 2.1.3 on 2020-05-06 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0043_auto_20200427_2108"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salespersoninvoice",
            name="invoice_sum",
            field=models.FloatField(default=0, null=True),
        ),
    ]
