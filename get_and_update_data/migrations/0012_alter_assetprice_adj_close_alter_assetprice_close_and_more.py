# Generated by Django 4.2.1 on 2023-06-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0011_alter_assetprice_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetprice',
            name='adj_close',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='close',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='high',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='low',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='open',
            field=models.DecimalField(decimal_places=10, max_digits=10),
        ),
        migrations.AlterField(
            model_name='assetprice',
            name='volume',
            field=models.BigIntegerField(),
        ),
    ]