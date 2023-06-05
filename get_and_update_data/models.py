from django.db import models
from django.core.exceptions import PermissionDenied

class AssetPrice(models.Model):
    
    datetime = models.DateTimeField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    adj_close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    run = models.DateTimeField()
    symbol = models.CharField()

    class Meta:
        db_table = 'assets_price'
        app_label = 'get_and_update_data'
        unique_together = (('symbol', 'datetime'), )

    def __str__(self):
        return self.symbol + "_" + self.datetime.strftime("%Y-%m-%d %H:%m")
    
class B3Companie(models.Model):

    symbol = models.CharField()
    minutes_update_rate = models.IntegerField()
    run = models.DateField(auto_now=True)

    class Meta:
        db_table = 'b3_companies'
        app_label = 'get_and_update_data'
        unique_together = (('symbol', 'run'), )

    def __str__(self):
        return self.symbol + "_" + self.run.strftime("%Y-%m-%d")
    
from django.contrib.auth.models import User
from datetime import datetime

class StockPortfolio(models.Model):

    SYMBOL_CHOICES = B3Companie.objects.values_list('symbol', flat=True).distinct()
    SYMBOL_CHOICES = [(value, value) for value in SYMBOL_CHOICES]

    symbol = models.CharField(max_length=10, choices=SYMBOL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    email = models.EmailField(null=True)
    username = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f"{self.symbol} - {self.date}"

    class Meta:

        permissions = [
            ("write_stockportfolio", "Can write to StockPortfolio"),
        ]

        db_table = 'users_stocks'
        app_label = 'get_and_update_data'
        unique_together = (('symbol', 'date', 'username'), )

    def save(self, *args, **kwargs):

        # Automatically fill the email and username fields with the user's information
        if not self.pk and self.username:
            self.email = self.email
            self.username = self.username
            if not self.date:
                self.date = datetime.now().strftime("%Y-%m-%d")
        super().save(*args, **kwargs)