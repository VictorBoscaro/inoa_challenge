from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import CompanyForm, LoginForm, RegistrationForm, StockPortfolioForm
from get_and_update_data.see_there_it_goes import LineChart, DataRetriever
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

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
        return render(request, 'asset_price.html', {'form': form})

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
            stock.date = datetime.now().date()
            stock.email = request.user.email
            stock.username = request.user.username
            stock.save()
            return redirect('asset')
        return render(request, 'add_stock.html', {'form': form})