from django.shortcuts import render
from customers.models import *
from rest_framework.generics import*
from customers.serializers import *
from rest_framework.views import *
from django.db.models import Q
from datetime import datetime
from rest_framework.response import Response

from rest_framework.exceptions import APIException # for define custom exception message

class CustomerRegistrationView(ListCreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomersRegistrationSerializer

class EditCustomerView(RetrieveUpdateAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomersRegistrationSerializer


class LoginCustomerView(ListCreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = LoginCustomerSerializer
    def create(self, request, *args, **kwargs):
        data= request.data
        try:
            login_data = Customers.objects.filter(
                Q(email=data["username"]) | Q(contact_no=data["username"]),
                password=data["password"])[:1]
            for data in login_data:
                request_data = {}
                data.last_login = datetime.now()
                data.save()
                request_data['user_id'] = data.id
                request_data['email'] = data.email
                request_data['contact_no'] = data.contact_no
                request_data['success'] = 1
            return Response(request_data)

        except Exception as e:
            print(e)
            raise APIException({
                'msg': 'You have entered an invalid username or password',
                'success': 0
            })



class MappingCustomerAndAppCreateView(CreateAPIView):
    queryset = CustomerAppMasterMapping.objects.all()
    serializer_class = CustomerAppMasterMappingSerializer

class CustomerDashbordReadView(RetrieveAPIView):
    queryset = Customers.objects.all()
    serializer_class = CustomerAppDetailsSerializer
    def get_queryset(self):
        customer_id = self.kwargs['pk']
        query_set = Customers.objects.filter(is_active=True,pk=customer_id)
        return query_set

class CustomerOrderDetailsView(RetrieveAPIView):
    queryset = Customers.objects.all()
    serializer_class= CustomerOrderDetailsSerializer



class AddCustomerByAppOwnerView(ListCreateAPIView):
    queryset = Customers.objects.all()
    serializer_class = UseAppCustomerMappingSerializer

