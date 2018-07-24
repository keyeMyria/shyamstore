from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework.response import Response
from app_messenger.serializers import *
from app_messenger.models import *


# Create your views here.
class AppMessengerCreateView(ListCreateAPIView):
    queryset = AppMessenger.objects.all()
    serializer_class = AppMessengerSerializer

class AppMessengerManageView(ListAPIView):
    queryset = AppMessenger.objects.all()
    serializer_class = AppMessengerSerializer