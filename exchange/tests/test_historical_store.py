import pytest
from datetime import date, timedelta
from exchange.tasks import load_historical_data
from exchange.models import CurrencyExchangeRate,CurrencyProvider, Currency

@pytest.mark.django_db  # Ensures the test uses a test database
def test_historical_data():
    CurrencyProvider.objects.create(
                          name="CurrencyBeacon",
                          is_active=True,
                          is_default=True,
                      )
    
    Currency.objects.create(
                          code="USD",
                          name='United State',
                          symbol="$",
                      )
    Currency.objects.create(
                          code="EUR",
                          name="Europe",
                          symbol="",
                      )
    Currency.objects.create(
                          code="GBP",
                          name="United Kingdom",
                          symbol="",
                      )
    Currency.objects.create(
                          code="CHF",
                          name=True,
                          symbol="",
                      )
    start_date = date.today() - timedelta(days=5)
    end_date = date.today()
    str_start_date = start_date.strftime('%Y-%m-%d')
    str_end_date = end_date.strftime('%Y-%m-%d')
    load_historical_data(str_start_date, str_end_date)
    
    # Assertions
    rates = CurrencyExchangeRate.objects.filter(valuation_date__range=(str_start_date, str_end_date))
    assert rates.count() > 0  # Expecting one rate per day in the 5-day range
