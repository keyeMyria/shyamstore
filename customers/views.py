from django.shortcuts import render
from customers.models import *
from rest_framework.generics import*
from customers.serializers import *
from rest_framework.views import *
from django.db.models import Q
from datetime import datetime

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
        request_data = {}
        data= request.data
        login_data = Customers.objects.filter(
            Q(email=data["username"]) | Q(contact_no=data["username"]),
            password=data["password"])[:1]
        if login_data:
            for data in login_data:
                data.last_login = datetime.now()
                data.save()
                request_data['user_id'] = data.id
                request_data['email'] = data.email
                request_data['contact_no'] = data.contact_no
                request_data['success'] = 1
        else:
            # request_data['error']=0
            request_data['error']="You have entered an invalid username or password"
        return Response(request_data)

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
