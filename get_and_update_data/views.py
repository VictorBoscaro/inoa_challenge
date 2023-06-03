import plotly.graph_objects as go
from django.shortcuts import render
from django.views.generic import View
from get_and_update_data.models import AssetPrice, B3Companie
from .forms import CompanyForm
from get_and_update_data.see_there_it_goes import LineChart, DataRetriever

# Create your views here.

class HomeView(View):

    def get(self, request):
        form = CompanyForm()
        return render(request, 'home.html', {'form': form})

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            # Process the form data
            company = form.cleaned_data['company']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # Perform further actions with the form data
            data_retriever = DataRetriever(company, start_date, end_date)
            dates, prices = data_retriever.retrieve_data()

            line_chart = LineChart(
                dates, 
                prices, 
                f"Preços do ativo {company} de {start_date} até {end_date}",
                "Data",
                "Preço"
            )
            
            json_fig = line_chart.plot_to_json()

            return render(request, 'home.html', {'form': form, 'plot_image': json_fig})

        return render(request, 'home.html', {'form': form})


class AssetPricesView(View):

    template_name = 'asset_price.html'
    def get(self, request):
        return render(request, 'asset_prices.html')
    
    def post(self, request):
        asset_name = request.POST.get('asset_name')
        asset_prices = AssetPrice.objects.filter(asset_name=asset_name).order_by('datetime')
        
        # Retrieve timestamps and prices from the queryset
        timestamps = [price.timestamp for price in asset_prices]
        prices = [price.price for price in asset_prices]

        b3_companies = list(B3Companie().objects.values_list('symbol', flat=True).distinct())

        return render(request, 'asset_prices.html', {'b3_companies': b3_companies})