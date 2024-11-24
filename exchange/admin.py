# exchange/admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Currency, CurrencyExchangeRate, CurrencyProvider
from .forms import CurrencyConversionForm
from .tasks import load_historical_data

admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
admin.site.register(CurrencyProvider)

# Admin view for currency conversion
def convert_currency_view(request):
    if request.method == 'POST':
        form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            converted_amount = form.get_converted_amount()
            return render(request, 'admin/convert_currency.html', {'form': form, 'converted_amount': converted_amount})
    else:
        form = CurrencyConversionForm()
    return render(request, 'admin/convert_currency.html', {'form': form})

# Adding custom URLs in the admin interface
# admin.site.urls += [
#     path('convert-currency/', convert_currency_view, name='convert_currency'),
# ]