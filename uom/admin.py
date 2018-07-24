from django.contrib import admin
from uom.models import *
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id','currency','value')