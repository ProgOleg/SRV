# Generated by Django 2.1.3 on 2019-09-10 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0040_salespersoninvoice_date_of_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="salespersoninvoice",
            name="invoice_sum",
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]
