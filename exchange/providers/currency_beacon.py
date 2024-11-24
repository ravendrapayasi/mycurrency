# exchange/providers/currency_beacon.py
import requests
from datetime import datetime
from asgiref.sync import sync_to_async

class CurrencyBeaconProvider:
    BASE_URL = 'https://api.currencybeacon.com/v1/'

    def __init__(self):
        self.api_key = 'kNsA8xQLtyoj6PzCmFvVI1uF1Onvs1k9'  # Replace with your actual CurrencyBeacon API key

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        url = f"{self.BASE_URL}latest"
        params = {
            'base': source_currency,
            'symbols': exchanged_currency,
        }
        if valuation_date:
            url = f"{self.BASE_URL}historical"
            params['date'] = valuation_date.strftime('%Y-%m-%d')
        response = requests.get(url, params=params, headers=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            rate = data['response']['rates'].get(exchanged_currency)
            if rate:
                return rate
            else:
                raise ValueError(f"No rate found for {source_currency} to {exchanged_currency} on {valuation_date}")
        else:
            raise ValueError(f"Error fetching data from CurrencyBeacon API: {response.text}")