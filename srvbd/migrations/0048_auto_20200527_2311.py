# Generated by Django 2.1.3 on 2020-05-27 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('srvbd', '0047_person_person_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='person_role',
            new_name='role',
        ),
    ]