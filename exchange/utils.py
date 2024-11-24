# exchange/utils.py
from .models import CurrencyProvider
from .providers.currency_beacon import CurrencyBeaconProvider
from .providers.mock import MockCurrencyProvider
from asgiref.sync import sync_to_async

@sync_to_async
def get_currency_rate_data(source_currency, exchanged_currency, valuation_date, provider=None):
    if provider is None:
        provider = CurrencyProvider.objects.filter(is_default=True, is_active=True).first()

    if provider is None:
        raise ValueError("No active provider available")
    if provider.name == 'CurrencyBeacon':
        provider_class = CurrencyBeaconProvider()
    elif provider.name == 'Mock':
        provider_class = MockCurrencyProvider()
    else:
        raise ValueError("Unknown provider")

    return provider_class.get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)

def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider=None):
    if provider is None:
        provider = CurrencyProvider.objects.filter(is_default=True, is_active=True).first()
    print(provider)
    if provider is None:
        raise ValueError("No active provider available")
    if provider.name == 'CurrencyBeacon':
        provider_class = CurrencyBeaconProvider()
    elif provider.name == 'Mock':
        provider_class = MockCurrencyProvider()
    else:
        raise ValueError("Unknown provider")

    return provider_class.get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)