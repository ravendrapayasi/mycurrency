# exchange/models.py
from django.db import models
from asgiref.sync import sync_to_async

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.code})"

class CurrencyProvider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField()
    rate_value = models.DecimalField(decimal_places=6, max_digits=18)

    def __str__(self):
        return f"{self.source_currency} to {self.exchanged_currency} on {self.valuation_date}"