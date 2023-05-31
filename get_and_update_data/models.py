from django.db import models

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