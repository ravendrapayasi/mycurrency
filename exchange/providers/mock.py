# exchange/providers/mock.py
import random
from datetime import datetime

class MockCurrencyProvider:
    
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        rate = round(random.uniform(0.5, 1.5), 6)
        return rate