# Generated by Django 4.2.1 on 2023-06-05 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0012_alter_assetprice_adj_close_alter_assetprice_close_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetprice',
            name='volume',
            field=models.DecimalField(decimal_places=10, max_digits=20),
        ),
    ]
