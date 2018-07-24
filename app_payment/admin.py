from django.contrib import admin
from  app_payment.models import AppPayment

@admin.register(AppPayment)
class AppPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'product_name','price')