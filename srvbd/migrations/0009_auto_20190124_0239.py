# Generated by Django 2.1.3 on 2019-01-24 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("srvbd", "0008_auto_20190116_2056"),
    ]

    operations = [
        migrations.AlterField(
            model_name="incoming",
            name="detail_incoming",
            field=models.ForeignKey(
                null=True, on_delete=None, related_name="detail_for_incom_list", to="srvbd.DetailInIncomList"
            ),
        ),
    ]
