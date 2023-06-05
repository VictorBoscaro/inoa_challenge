from django.urls import path
from .views import AssetView, HomeView, RegistrationView, AddStockView

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('asset_price/', AssetView.as_view(), name='asset'),
    path('registration/', RegistrationView.as_view(), name = 'registration'),
    path('add_stock/', AddStockView.as_view(), name='add_stock'),
    # Add other URL patterns as needed
]
