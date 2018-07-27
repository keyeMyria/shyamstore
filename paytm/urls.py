from django.conf.urls import include, url
from django.urls import include, path
from paytm import views
from rest_framework import routers
# urlpatterns = [
#     # Examples:
#     url(r'^$', 'paytm.views.home', name='home'),
#     url(r'^payment/', 'paytm.views.payment', name='payment'),
#     url(r'^response/', 'paytm.views.response', name='response'),
# ]

urlpatterns = [
    # Examples:
    path('', views.home, name='home'),
    path('payment/', views.payment, name='payment'),
    path('response/', views.response, name='response'),


    path('payment_request/',views.PaymentRequestView.as_view()),
    path('get_payment_details/',views.GetPaymentDetailsView.as_view())
]
