# Generated by Django 4.2.1 on 2023-06-14 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0020_emailrecord'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='emailrecord',
            table='emails_sent',
        ),
    ]
