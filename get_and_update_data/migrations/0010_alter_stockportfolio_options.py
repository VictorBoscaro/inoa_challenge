# Generated by Django 4.2.1 on 2023-06-05 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0009_alter_stockportfolio_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockportfolio',
            options={'permissions': [('write_stockportfolio', 'Can write to StockPortfolio')]},
        ),
    ]
