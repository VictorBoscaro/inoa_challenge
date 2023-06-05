# Generated by Django 4.2.1 on 2023-06-05 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0007_alter_stockportfolio_table'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stockportfolio',
            unique_together={('symbol', 'date')},
        ),
        migrations.RemoveField(
            model_name='stockportfolio',
            name='email',
        ),
        migrations.RemoveField(
            model_name='stockportfolio',
            name='username',
        ),
    ]
