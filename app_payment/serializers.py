from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_payment.models import *

class PriceDetailsSerializer(ModelSerializer):

    class Meta:
        model=AppPayment
        fields="__all__"
