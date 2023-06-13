from django.urls import path
from .views import AssetView, HomeView, RegistrationView, AddStockView, StockUpdateView, GetDatesView, AddCompanieView, UpdateDatabase

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('asset_price/', AssetView.as_view(), name='asset'),
    path('registration/', RegistrationView.as_view(), name = 'registration'),
    path('add_stock/', AddStockView.as_view(), name='add_stock'),
    path('update_stock/', StockUpdateView.as_view(), name='update_stock'),
    path('get_dates/', GetDatesView.as_view(), name = 'get_dates'),
    path('add_companie/', AddCompanieView.as_view(), name='add_companie'),
    path('asset_price/', UpdateDatabase.as_view(), name='update_stock'),
]
