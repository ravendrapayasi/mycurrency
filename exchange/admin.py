# exchange/admin.py
from django.contrib import admin
from django.urls import path
from .models import Currency, CurrencyExchangeRate, CurrencyProvider
from .views import convert_currency_view

admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
admin.site.register(CurrencyProvider)

# # Register the custom view in Django admin
class CurrencyConvertAdmin(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('convert_currency/', self.admin_view(convert_currency_view), name='admin_convert_currency')  # Custom URL for conversion
        ]
        return custom_urls + urls

admin_site = CurrencyConvertAdmin(name='CorrencyConvertAdmin')

# Register all models from the default admin site to the custom admin site
for model in admin.site._registry:
    admin_site.register(model, admin.site._registry[model].__class__)