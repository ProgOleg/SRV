# Generated by Django 2.1.3 on 2020-09-04 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0053_auto_20200904_0414"),
    ]

    operations = [
        migrations.AddField(
            model_name="materialsaleobject",
            name="own_margin",
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name="materialsaleobject",
            name="repair_invoice_attach",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="material_repair_invoice",
                to="srvbd.RepairInvoice",
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="role",
            field=models.CharField(
                choices=[("MA", "Мастер"), ("CL", "Клиент"), ("OW", "Собственник")], default="CL", max_length=2
            ),
        ),
    ]
