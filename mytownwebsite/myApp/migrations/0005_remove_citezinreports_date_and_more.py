# Generated by Django 5.0.3 on 2024-04-04 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_remove_addreport_facility_addreport_facility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citezinreports',
            name='date',
        ),
        migrations.RemoveField(
            model_name='managerreports',
            name='date',
        ),
    ]
