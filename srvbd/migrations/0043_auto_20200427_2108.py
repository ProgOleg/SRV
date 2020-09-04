# Generated by Django 2.1.3 on 2020-04-27 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0042_auto_20200427_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='incoming_price',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='detail',
            name='quantity',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='detailinincomlist',
            name='incoming_price',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='detailinincomlist',
            name='quantity',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='exchangerates',
            name='exchange_rates',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='materialsaleobject',
            name='quantity',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='materialsaleobject',
            name='sale_price',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='repairinvoice',
            name='invoice_sum',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='virtualsaleobject',
            name='quantity',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='virtualsaleobject',
            name='sale_price',
            field=models.FloatField(default=0, null=True),
        ),
    ]
