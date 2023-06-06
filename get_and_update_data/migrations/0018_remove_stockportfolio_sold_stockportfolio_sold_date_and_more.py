# Generated by Django 4.2.1 on 2023-06-06 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0017_stockportfolio_sold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockportfolio',
            name='sold',
        ),
        migrations.AddField(
            model_name='stockportfolio',
            name='sold_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='stockportfolio',
            name='sold_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
