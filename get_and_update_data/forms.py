from django import forms
from .models import B3Companie, StockPortfolio
from django.contrib.auth.models import Group, User

class CompanyForm(forms.Form):
    company = forms.CharField(label="Ativo")
    start_date = forms.DateField(label="Data Inicial")
    end_date = forms.DateField(label="Data Final")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_values = B3Companie.objects.values_list('symbol', flat=True).distinct()
        choices = [(value, value) for value in unique_values]
        self.fields['company'].widget = forms.Select(choices=choices)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegistrationForm(forms.Form):

    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
    def save(self):
            
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            email = self.cleaned_data['email']

            # Create the user account
            user = User.objects.create_user(username=username, password=password, email=email)

            # Assign the user to the stock group
            stock_group = Group.objects.get(name='Stock Users')
            user.groups.add(stock_group)

            return user
    
class StockPortfolioForm(forms.ModelForm):
    class Meta:
        model = StockPortfolio
        fields = ('symbol', 'price', 'date')