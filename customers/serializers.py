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


class CustomerAppMasterMappingSerializer(ModelSerializer):
    class Meta:
        model=CustomerAppMasterMapping
        fields = ['id','customer','app_master']
    def create(self, validated_data):
        customer_id = validated_data.get("customer")
        app_master_id = validated_data.get("app_master")
        customer_mapping_data = CustomerAppMasterMapping.objects.filter(customer_id=customer_id,app_master_id=app_master_id)[:1]

        if customer_mapping_data:
            for data in customer_mapping_data:
                if data.is_active:
                    data.is_active = False
                else:
                    data.is_active = True
                data.save()
                mapping_data = data
        else:
            mapping_data=CustomerAppMasterMapping.objects.create(**validated_data)


        return mapping_data


class CustomerAppDetailsSerializer(ModelSerializer):

    class Meta:
        model = Customers
        # fields = ['id','customer_name','email','contact_no','app_master']
        fields = ['app_master']
