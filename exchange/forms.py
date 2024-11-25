# exchange/forms.py
from django import forms
from .models import Currency
from .utils import get_exchange_rate_data

class CurrencyConversionForm(forms.Form):
    source_currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    exchanged_currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    amount = forms.DecimalField(max_digits=18, decimal_places=2)

    def clean(self):
        cleaned_data = super().clean()
        source_currency = cleaned_data.get('source_currency')
        exchanged_currency = cleaned_data.get('exchanged_currency')
        
        if source_currency == exchanged_currency:
            raise forms.ValidationError("Source and target currencies must be different.")
        return cleaned_data

    def get_converted_amount(self):
        cleaned_data = self.cleaned_data
        source_currency = cleaned_data.get("source_currency")
        exchanged_currency = cleaned_data.get("exchanged_currency")
        amount = cleaned_data.get("amount")
        
        rate = get_exchange_rate_data(
            source_currency=source_currency.code,
            exchanged_currency=exchanged_currency.code,
            valuation_date=None,
            provider=None  # Default provider will be used
        )
        
        return rate * float(amount)