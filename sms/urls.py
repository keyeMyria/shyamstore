from sms import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('send_sms/',views.SEMSendView.as_view()),
    #path('sms/', views.SMSView, name='SMSView'),
    #path('send_sms/', views.SEMSendView, name='SEMSendView'),
    #path('all_categories/<pk>/',views.CategoryByIdReadView.as_view())


]