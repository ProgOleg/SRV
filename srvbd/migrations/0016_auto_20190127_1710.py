# Generated by Django 2.1.3 on 2019-01-27 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0015_remove_incoming_detail_incoming'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incoming',
            old_name='statys',
            new_name='status',
        ),
    ]
