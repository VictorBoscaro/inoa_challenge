# Generated by Django 4.2.1 on 2023-06-05 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0016_alter_assetprice_adj_close_alter_assetprice_close_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockportfolio',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]