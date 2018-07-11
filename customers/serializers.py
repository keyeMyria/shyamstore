from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from customers.models import *
from django.db.models import Q


class CustomersRegistrationSerializer(ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"

class LoginCustomerSerializer(ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = Customers
        fields = ['username','password']
