# Generated by Django 2.1.3 on 2019-03-17 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0025_auto_20190317_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialsaleobject',
            name='person_invoice_attach',
            field=models.ForeignKey(default=None, null=True, on_delete=None, related_name='material_person_invoice', to='srvbd.SalesPersonInvoice'),
        ),
        migrations.AlterField(
            model_name='materialsaleobject',
            name='repair_invoice_attach',
            field=models.ForeignKey(default=None, null=True, on_delete=None, related_name='material_repair_invoice', to='srvbd.RepairInvoice'),
        ),
    ]
