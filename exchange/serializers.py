# exchange/serializers.py
from rest_framework import serializers
from .models import Currency, CurrencyExchangeRate

# Serializer for Currency model
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol']

# Serializer for CurrencyExchangeRate model
class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    source_currency = CurrencySerializer()  # Nested CurrencySerializer for source_currency
    exchanged_currency = CurrencySerializer()  # Nested CurrencySerializer for exchanged_currency

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']