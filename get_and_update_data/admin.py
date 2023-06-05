from django.contrib import admin
from .models import AssetPrice, B3Companie, StockPortfolio
from datetime import datetime

class StockPortfolioAdmin(admin.ModelAdmin):
    readonly_fields = ('date', 'email', 'username')
    fields = ('symbol', 'price')
    
    def save_model(self, request, obj, form, change):
        obj.date = datetime.now()
        obj.email = request.user.email
        obj.username = request.user.username
        obj.save()


# Register your models here.
admin.site.register(AssetPrice)
admin.site.register(B3Companie)
admin.site.register(StockPortfolio, StockPortfolioAdmin)