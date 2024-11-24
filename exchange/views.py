# exchange/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Currency
from .serializers import CurrencySerializer
from .forms import CurrencyConversionForm
from .utils import get_exchange_rate_data,get_currency_rate_data
from datetime import datetime, timedelta
from .tasks import async_load_historical_data
import asyncio
import time
from adrf.views import APIView  as aAPIView
from django.conf import settings
from .rabbitmq_utils import publish_message
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

# View to list all currencies
class CurrencyListView(APIView):
    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data)
    
class ExchangeRateListView(APIView):
    def get(self, request):
        """message = request.data.get('message', 'Default message')
        queue_name = settings.RABBITMQ_QUEUE

        try:
            publish_message(queue_name, message)
            return Response({"status": "Message sent", "message": message})
        except Exception as e:
            return Response({"status": "Error", "error": str(e)}, status=500)"""
        
        source_currency = request.query_params.get('source_currency')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not all([source_currency, start_date, end_date]):
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch exchange rates using the utility function
        exchange_rates = []
        current_date = start_date
        exchanged_currency = 'USD'
        while current_date <= end_date:
            rate = get_exchange_rate_data(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=current_date,
                provider=None  # Use the default provider
            )
            #rate = 
            exchange_rates.append({
                'valuation_date': current_date.strftime('%Y-%m-%d'),
                'rate_value': rate
            })
            current_date += timedelta(days=1)

        if exchange_rates:
            message = {"start_date":start_date.strftime('%Y-%m-%d'),"end_date":end_date.strftime('%Y-%m-%d')}
            queue_name = settings.RABBITMQ_QUEUE
            publish_message(queue_name, message)
            return Response({"message": "Successfully Fetched data","exchange_rates":exchange_rates})
        else:
            return Response({"message": "No data found for the given period"}, status=status.HTTP_404_NOT_FOUND)


# View to get exchange rate history for a time period
class CurrencyRateHistoryView(aAPIView):
    async def get(self, request):
        source_currency = request.query_params.get('source_currency')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not all([source_currency, start_date, end_date]):
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch exchange rates using the utility function
        exchange_rates = []
        current_date = start_date
        exchanged_currency = 'USD'
        while current_date <= end_date:
            rate = await asyncio.gather(get_currency_rate_data(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=current_date,
                provider=None  # Use the default provider
            ))
            #rate = 
            exchange_rates.append({
                'valuation_date': current_date.strftime('%Y-%m-%d'),
                'rate_value': rate
            })
            current_date += timedelta(days=1)

        if exchange_rates:
            start_time = time.time()
            result = await asyncio.gather(async_load_historical_data(source_currency,exchanged_currency,exchange_rates))
            total = time.time()-start_time
            return Response({"message": "Successfully Fetched data","exchange_rates":exchange_rates,"result":result,"total":total})
        else:
            return Response({"message": "No data found for the given period"}, status=status.HTTP_404_NOT_FOUND)
        
        

# View to perform currency conversion
class CurrencyConverterView(APIView):
    def post(self, request):
        source_currency = request.data.get('source_currency')
        exchanged_currency = request.data.get('exchanged_currency')
        amount = request.data.get('amount')

        if not all([source_currency, exchanged_currency, amount]):
            return Response({"error": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get exchange rate data from the utility function
            rate = get_exchange_rate_data(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=None,  # No date means use the latest rate
                provider=None  # Use default provider
            )

            # Calculate the converted amount
            converted_amount = float(amount) * rate
            return Response({"converted_amount": converted_amount})

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Admin view for currency conversion
@staff_member_required
def convert_currency_view(request):
    if request.method == 'POST':
        form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            converted_amount = form.get_converted_amount()
            return render(request, 'admin/convert_currency.html', {'form': form, 'converted_amount': converted_amount})
    else:
        form = CurrencyConversionForm()
    return render(request, 'admin/convert_currency.html', {'form': form})
