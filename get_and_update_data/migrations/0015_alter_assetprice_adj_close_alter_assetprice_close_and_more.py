# Generated by Django 4.2.1 on 2023-06-05 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0014_alter_assetprice_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetprice',
            name='adj_close',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='close',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='high',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='low',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='open',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='volume',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
    ]
