# Generated by Django 4.2.1 on 2023-06-05 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_and_update_data', '0004_rename_b3companies_b3companie'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockPortfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(choices=[('PETR4.SA', 'PETR4.SA'), ('USIM5.SA', 'USIM5.SA'), ('ENBR3.SA', 'ENBR3.SA'), ('BRKM5.SA', 'BRKM5.SA'), ('BBDC4.SA', 'BBDC4.SA'), ('KLBN11.SA', 'KLBN11.SA'), ('BBAS3.SA', 'BBAS3.SA'), ('LREN3.SA', 'LREN3.SA'), ('MULT3.SA', 'MULT3.SA'), ('BBDC3.SA', 'BBDC3.SA'), ('CMIG4.SA', 'CMIG4.SA'), ('SBSP3.SA', 'SBSP3.SA'), ('ITSA4.SA', 'ITSA4.SA'), ('OIBR4.SA', 'OIBR4.SA'), ('RADL3.SA', 'RADL3.SA'), ('CCRO3.SA', 'CCRO3.SA'), ('JBSS3.SA', 'JBSS3.SA'), ('PETR3.SA', 'PETR3.SA'), ('UGPA3.SA', 'UGPA3.SA'), ('ECOR3.SA', 'ECOR3.SA'), ('BBSE3.SA', 'BBSE3.SA'), ('EQTL3.SA', 'EQTL3.SA')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=150)),
            ],
        ),
    ]
