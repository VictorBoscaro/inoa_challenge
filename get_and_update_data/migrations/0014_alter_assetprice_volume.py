# Generated by Django 4.2.1 on 2023-06-05 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0013_alter_assetprice_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetprice',
            name='volume',
            field=models.DecimalField(decimal_places=15, max_digits=20),
        ),
    ]