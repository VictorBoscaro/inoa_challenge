from django.urls import path
from .views import AssetView, HomeView, RegistrationView

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('asset_price/', AssetView.as_view(), name='asset'),
    path('registration/', RegistrationView.as_view(), name = 'registration')
    # Add other URL patterns as needed
]
