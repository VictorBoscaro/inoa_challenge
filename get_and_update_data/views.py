from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from .forms import CompanyForm, LoginForm, RegistrationForm, StockPortfolioForm, UpdateStockForm, B3CompanieForm
from get_and_update_data.see_there_it_goes import LineChart, DataRetriever
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import StockPortfolio, AssetPrice
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django_pandas.io import read_frame
from django.http import JsonResponse
from datetime import timedelta, datetime
import pandas as pd

class HomeView(FormView):
    template_name = 'home.html'
    form_class = LoginForm
    success_url = '/asset_price/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = RegistrationForm()
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            form.add_error(None, 'Invalid username or password')
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if 'register' in request.POST:
            return redirect('registration')
        return super().post(request, *args, **kwargs)

from django.contrib.auth.models import Group

class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            form.add_error('email', 'This email is already registered.')
            return self.form_invalid(form)

        if User.objects.filter(username=username).exists():
            form.add_error('username', 'This username is already registered.')
            return self.form_invalid(form)

        user = User.objects.create_user(username=username, password=password, email=email)

        # Assign the user to the desired group
        group = Group.objects.get(name='StockPortfolio Writers')  # Replace 'your_group_name' with the actual group name
        group.user_set.add(user)

        return redirect(self.success_url)

class AssetView(View):

    def get(self, request):
        form = CompanyForm()
        assets = StockPortfolio.objects.filter(username=request.user, sold_date__isnull=True)

        for asset in assets:
            last_data_point = AssetPrice.objects.filter(symbol=asset.symbol, granularity='1d').order_by('-datetime').first()
            if last_data_point:
                asset.current_price = round(last_data_point.close, 2)
                asset.gain_loss = f"{round(((asset.current_price - asset.price)/asset.price), 2) * 100}%"
            else:
                asset.current_price = None
                asset.gain_loss = None
        return render(request, 'asset_price.html', {'form': form, 'assets':assets})

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            # Process the form data
            company = form.cleaned_data['company']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            granularity = form.cleaned_data['granularity']
            moving_average = form.cleaned_data['moving_average']

            # Perform further actions with the form data
            data_retriever = DataRetriever(company, start_date, end_date, granularity)
            dates, prices = data_retriever.retrieve_data()

            line_chart = LineChart(
                dates, 
                prices, 
                moving_average,
                f"Preços do ativo {company} de {start_date} até {end_date}",
                "Data",
                "Preço"
            )
            
            json_fig = line_chart.plot_to_json()

            return render(request, 'asset_price.html', {'form': form, 'plot_image': json_fig})

        return render(request, 'asset_price.html', {'form': form})

class AddStockView(LoginRequiredMixin, View):

    def get(self, request):
        form = StockPortfolioForm()
        return render(request, 'add_stock.html', {'form': form})

    def post(self, request):
        form = StockPortfolioForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.email = request.user.email
            stock.username = request.user.username
            stock.save()
            return redirect('asset')
        return render(request, 'add_stock.html', {'form': form})

class StockUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateStockForm()
        return render(request, 'update_stock.html', {'form': form})

    def post(self, request):
        form = UpdateStockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            date = form.cleaned_data['date']
            sold_date = form.cleaned_data['sold_date']
            sold_price = form.cleaned_data['sold_price']
            username = request.user.username

            stock = get_object_or_404(StockPortfolio, symbol=symbol, date=date, username=username)
            stock.sold_date = sold_date
            stock.sold_price = sold_price
            stock.save()

            return redirect('asset')

        return render(request, 'update_stock.html', {'form': form})
    

class EmailSelector:

    # def __init__(self):

    #     self.symbol = symbol

    def purchase_email(self, model = User):
        
        all_email = model.objects.values_list('email', flat=True).distinct()
        all_email = [email for email in all_email]
        return all_email
    
    # def sell_email(self, model = StockPortfolio):
    #     if self.symbol == None:
    #         raise ValueError("Insert a symbol when instantiting the class")
    #     else:
    #         users_with_stock = model.objects.filter(symbol = self.symbol).values_list('email', flat=True).distinct()
    #         users_with_stock = [email for email in users_with_stock]
    #         return users_with_stock

class EmailSender(View):

    def __init__(self, subject, message, email_list, from_email = 'inoachallengetest@gmail.com'):

        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.email_list = email_list

    def send_email_to_user(self):
        
        send_mail(self.subject, self.message, self.from_email, self.email_list)

class RecommendationRule:

    LAST_60_DAYS = datetime.today() - timedelta(60)

    def __init__(self, users_model = StockPortfolio, asset_model = AssetPrice):

        self.users_model = users_model
        self.asset_model = asset_model

    def purchase_rule(self, moving_average, var_threshold, last_days = LAST_60_DAYS):

        model_data = self.asset_model.objects.filter(granularity='1d', datetime__gte=last_days).all()
        model_data_df = read_frame(model_data)
        model_data_df['datetime'] = model_data_df.datetime.apply(lambda x: x.replace(tzinfo=None))
        model_data_df['moving_average'] = model_data_df.groupby('symbol')['close'].\
            transform(lambda x: x.rolling(window=moving_average).mean())
        
        last_moving_average = model_data_df[(model_data_df['datetime'] < model_data_df['datetime'].max())].groupby('symbol')['moving_average'].last()

        last_price = model_data_df.groupby('symbol').close.last()
        comp_df = pd.merge(left = last_price, right = last_moving_average, left_index = True, right_index = True)
        comp_df['close'] = comp_df['close'].astype(float)
        comp_df['variation'] = (comp_df['close'] - comp_df['moving_average'])/comp_df['moving_average']
        stocks_rec = comp_df[comp_df['variation'] <= var_threshold].index
        
        return list(stocks_rec)
    
    def sell_rule(self, sell_threshold = 0.1):

        # Get all unsold stocks from the users' portfolios
        portfolios = self.users_model.objects.filter(sold_date__isnull=True).all()
        portfolios_df = pd.DataFrame(list(portfolios.values()))

        # Get the latest asset prices
        latest_prices = self.asset_model.objects.filter(granularity='1d').order_by('symbol', '-datetime').distinct('symbol')
        latest_prices_df = pd.DataFrame(list(latest_prices.values()))

        # Merge the two dataframes
        comp_df = pd.merge(left = portfolios_df, right = latest_prices_df, left_on = 'symbol', right_on = 'symbol')

        # Calculate the percentage change
        comp_df['perc_change'] = (comp_df['close'].astype(float) - comp_df['price'].astype(float))/comp_df['price'].astype(float)
        
        # Check the sell condition
        sell_recommendation = comp_df[comp_df['perc_change'] >= sell_threshold]

        # Return the emails and symbols of the stocks to be sold
        return sell_recommendation[['email', 'symbol']]
        
class GetDatesView(View):

    def get(self, request, *args, **kwargs):
        symbol = request.GET.get('symbol', None)
        user_email = request.user.email
        dates = StockPortfolio.objects.filter(symbol=symbol, email=user_email).values_list('date', flat=True)
        if dates:    
            date_list = [date.strftime("%Y-%m-%d") for date in dates]

            data = {
                "is_taken": True,
                "dates_list": date_list
            }
            return JsonResponse(data)
        
        else:
            data = {
                "is_taken": False,
            }
            return JsonResponse(data)

class AddCompanieView(View):
    form_class = B3CompanieForm
    template_name = 'add_companie.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset')
        return render(request, self.template_name, {'form': form})