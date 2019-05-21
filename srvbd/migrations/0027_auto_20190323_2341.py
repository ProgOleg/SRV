# Generated by Django 2.1.3 on 2019-03-23 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0026_auto_20190317_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_create', models.DateField(auto_now_add=True)),
                ('exchange_rates', models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True)),
                ('status_own_change', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameField(
            model_name='repairinvoice',
            old_name='stays',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='salespersoninvoice',
            old_name='stays',
            new_name='status',
        ),
        migrations.RemoveField(
            model_name='incoming',
            name='exchange_rates',
        ),
        migrations.AddField(
            model_name='incoming',
            name='exchange_ratest',
            field=models.ForeignKey(default=None, null=True, on_delete=None, related_name='incoming_exchange_rates', to='srvbd.ExchangeRates'),
        ),
        migrations.AddField(
            model_name='repairinvoice',
            name='exchange_rates',
            field=models.ForeignKey(default=None, null=True, on_delete=None, related_name='repair_exchange_rates', to='srvbd.ExchangeRates'),
        ),
        migrations.AddField(
            model_name='salespersoninvoice',
            name='exchange_rates',
            field=models.ForeignKey(default=None, null=True, on_delete=None, related_name='sale_person_exchange_rates', to='srvbd.ExchangeRates'),
        ),
    ]
