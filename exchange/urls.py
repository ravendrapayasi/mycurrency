# exchange/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('currencies/', views.CurrencyListView.as_view(), name='currency_list'),
    path('currency-rates-list/', views.CurrencyRateHistoryView.as_view(), name='currency_rate_history'),
    path('convert/', views.CurrencyConverterView.as_view(), name='currency_converter'),
    path('exchange-rates-list/', views.ExchangeRateListView.as_view(), name='exchange_rates_list'),
]
