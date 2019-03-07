# Generated by Django 2.1.3 on 2019-01-24 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0011_incoming_statys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailinlist',
            name='detail_name',
            field=models.ForeignKey(null=True, on_delete=None, related_name='detail_detail_in_list', to='srvbd.SparPart'),
        ),
        migrations.AlterField(
            model_name='detailinlist',
            name='selector_incom',
            field=models.ForeignKey(null=True, on_delete=None, related_name='select_incom', to='srvbd.Incoming'),
        ),
    ]
