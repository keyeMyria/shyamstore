from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from customers.models import *
from django.db.models import Q
from orders.serializers import OrdersSerializer


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



class CustomerOrderDetailsSerializer(ModelSerializer) :
    customer_details=OrdersSerializer(many=True)
    class Meta:
        model = Customers
        fields = ['id','customer_name','email','contact_no','customer_details']

class UseAppCustomerMappingSerializer(ModelSerializer):
    user = serializers.IntegerField()
    app_master = serializers.IntegerField()
    class Meta:
        model = Customers
        fields = ['id','customer_name','email','contact_no','password','user', 'app_master']

    def create(self, validated_data):
        data_dict = {}
        user = validated_data.pop('user')
        app_master = validated_data.pop('app_master')
        email = validated_data.get('email')
        contact_no = validated_data.get('contact_no')
        customer_existing = Customers.objects.filter(email = email, contact_no = contact_no)


        if customer_existing:
            for c_existing in customer_existing:
                data_dict['id'] = c_existing.id
                data_dict['customer_name'] = c_existing.customer_name
                data_dict['email'] = c_existing.email
                data_dict['contact_no'] = c_existing.contact_no
                data_dict['password'] = c_existing.password

        else:
            add_customer = Customers.objects.create(**validated_data)
            data_dict['id'] = add_customer.id
            data_dict['customer_name'] = add_customer.customer_name
            data_dict['email'] = add_customer.email
            data_dict['contact_no'] = add_customer.contact_no
            data_dict['password'] = add_customer.password

        UseAppCustomerMapping_existing = CustomerAppMasterMapping.objects.filter(app_master_id=app_master,
                                                                                 customer_id=data_dict['id'])

        if not UseAppCustomerMapping_existing:
            add_maping = CustomerAppMasterMapping.objects.create(app_master_id=app_master,
                                                     customer_id=data_dict['id'],
                                                     referred_by_id=user)
            data_dict['user'] = add_maping.referred_by.id
            data_dict['app_master'] = add_maping.app_master.id
        else:
            for c_ac_mapping in UseAppCustomerMapping_existing:
                data_dict['user'] =c_ac_mapping.referred_by_id
                data_dict['app_master'] =c_ac_mapping.app_master_id

        return data_dict

