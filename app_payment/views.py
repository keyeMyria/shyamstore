from django.shortcuts import render
from app_payment.serializers import *
from rest_framework.generics import*
from rest_framework.views import *
from rest_framework import filters
# Create your views here.
class AllProductPriceDetailsReadView(ListAPIView):
    queryset = AppPayment.objects.all()
    serializer_class = PriceDetailsSerializer