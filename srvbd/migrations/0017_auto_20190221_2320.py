# Generated by Django 2.1.3 on 2019-02-21 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0016_auto_20190127_1710"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date_create", models.DateTimeField(auto_now_add=True)),
                ("text", models.TextField(max_length=2000, verbose_name="Коментарий")),
            ],
        ),
        migrations.CreateModel(
            name="Device",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mod", models.CharField(max_length=50, verbose_name="Модель")),
                ("serial_number", models.CharField(max_length=50, verbose_name="Серийный номер")),
                ("pnc", models.CharField(max_length=50, verbose_name="PNC-код")),
                (
                    "manufacturer",
                    models.ForeignKey(
                        null=True, on_delete=None, related_name="device_manufacturer", to="srvbd.Manufacturer"
                    ),
                ),
                (
                    "type_appliances",
                    models.ForeignKey(
                        null=True, on_delete=None, related_name="device_type_appliances", to="srvbd.TypeAppliances"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DeviceUnderRepair",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type_of_repair",
                    models.CharField(choices=[("OU", "выездная"), ("IN", "в сервисе")], default="IN", max_length=2),
                ),
                ("external_condition", models.CharField(max_length=500, verbose_name="Внешнее стостояние")),
                ("date_create", models.DateTimeField(auto_now_add=True)),
                ("date_ready", models.DateTimeField()),
                ("date_delivery", models.DateTimeField()),
                ("status_ready", models.BooleanField(default=False)),
                ("status_delivery", models.BooleanField(default=False)),
                (
                    "comment",
                    models.ForeignKey(blank=True, on_delete=None, related_name="device_comment", to="srvbd.Comment"),
                ),
                (
                    "device_attach",
                    models.ForeignKey(on_delete=None, related_name="device_in_repair", to="srvbd.Device"),
                ),
                ("person_attach", models.ForeignKey(on_delete=None, related_name="device_person", to="srvbd.Person")),
            ],
        ),
        migrations.CreateModel(
            name="MaterialSaleObject",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=6)),
                ("sale_price", models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ("detail_attach", models.ForeignKey(on_delete=None, related_name="material_sale", to="srvbd.Detail")),
            ],
        ),
        migrations.CreateModel(
            name="RepairInvoice",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("invoice_sum", models.DecimalField(decimal_places=2, max_digits=6)),
                ("stays", models.BooleanField(default=False)),
                (
                    "repair_attach",
                    models.ForeignKey(on_delete=None, related_name="detail_invoice", to="srvbd.DeviceUnderRepair"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SalesPersonInvoice",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("invoice_sum", models.DecimalField(decimal_places=2, max_digits=6)),
                ("date_create", models.DateTimeField(auto_now_add=True)),
                ("stays", models.BooleanField(default=False)),
                ("person_attach", models.ForeignKey(on_delete=None, related_name="detail_sale", to="srvbd.Person")),
            ],
        ),
        migrations.CreateModel(
            name="VirtualSaleObject",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=6)),
                ("sale_price", models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                (
                    "person_invoice_attach",
                    models.ForeignKey(
                        default=None,
                        on_delete=None,
                        related_name="virtual_person_invoice",
                        to="srvbd.SalesPersonInvoice",
                    ),
                ),
                (
                    "repair_invoice_attach",
                    models.ForeignKey(
                        default=None, on_delete=None, related_name="virtual_repair_invoice", to="srvbd.RepairInvoice"
                    ),
                ),
                (
                    "spar_part_attach",
                    models.ForeignKey(on_delete=None, related_name="virtual_sale", to="srvbd.SparPart"),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="detailinincomlist",
            name="detail_name",
        ),
        migrations.DeleteModel(
            name="DetailInIncomList",
        ),
        migrations.AddField(
            model_name="materialsaleobject",
            name="person_invoice_attach",
            field=models.ForeignKey(
                default=None, on_delete=None, related_name="material_person_invoice", to="srvbd.SalesPersonInvoice"
            ),
        ),
        migrations.AddField(
            model_name="materialsaleobject",
            name="repair_invoice_attach",
            field=models.ForeignKey(
                default=None, on_delete=None, related_name="material_repair_invoice", to="srvbd.RepairInvoice"
            ),
        ),
    ]
