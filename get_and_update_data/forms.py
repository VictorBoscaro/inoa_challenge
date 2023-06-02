from django import forms
from .models import B3Companie, AssetPrice

class CompanyForm(forms.Form):
    company = forms.ChoiceField(choices=(), label = "Ativo")
    start_date = forms.DateField(label = "Data Inicial")
    end_date = forms.DateField(label = "Data Final")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_values = AssetPrice.objects.values_list('symbol', flat=True).distinct()
        choices = [(value, value) for value in unique_values]
        self.fields['company'].choices = choices
