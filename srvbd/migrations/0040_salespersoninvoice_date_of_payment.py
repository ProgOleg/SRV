# Generated by Django 2.1.3 on 2019-06-24 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0039_salespersoninvoice_payment_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="salespersoninvoice",
            name="date_of_payment",
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
