from django import forms
from .models import B3Companie, AssetPrice

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
