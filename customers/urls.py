from django.urls import path
from customers.views import *

urlpatterns = [
    path('customer_registration/', CustomerRegistrationView.as_view()),
    path('edit_customer/<pk>/', EditCustomerView.as_view()),
    path('customer_login/', LoginCustomerView.as_view()),
]