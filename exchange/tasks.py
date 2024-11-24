# exchange/tasks.py

from .models import Currency,CurrencyExchangeRate
from .utils import get_exchange_rate_data
from datetime import datetime, timedelta
import logging
import asyncio
from asgiref.sync import sync_to_async
import time
import tracemalloc
tracemalloc.start()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@sync_to_async
def async_load_historical_data(source_currency,exchanged_currency,exchange_rates):
    #asyncio.sleep(10)
    # Fetch the Currency instance for 'INR'
    source_currency_instance = Currency.objects.get(code='INR')
    exchanged_currency_instance = Currency.objects.get(code='USD')
    for exchange in exchange_rates:
        CurrencyExchangeRate.objects.create(
                            source_currency=source_currency_instance,
                            exchanged_currency=exchanged_currency_instance,
                            valuation_date=exchange['valuation_date'],
                            rate_value=exchange['rate_value'][0]
                        )
    return True

def load_historical_data(start_date, end_date):
    logger.info("start_date {start_date} end_date {end_date}")
    currencies = ['USD', 'EUR', 'GBP', 'CHF']
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    for date in (start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)):
        for source_currency in currencies:
            for exchanged_currency in currencies:
                if source_currency != exchanged_currency:
                    try:
                        rate = get_exchange_rate_data(source_currency, exchanged_currency, date)
                        source_currency_instance = Currency.objects.get(code=source_currency)
                        exchanged_currency_instance = Currency.objects.get(code=exchanged_currency)
                        CurrencyExchangeRate.objects.create(
                            source_currency=source_currency_instance,
                            exchanged_currency=exchanged_currency_instance,
                            valuation_date=date.strftime('%Y-%m-%d'),
                            rate_value=rate
                        )
                    except Exception as e:
                        print(f"Error fetching data for {source_currency} to {exchanged_currency} on {date}: {e}")