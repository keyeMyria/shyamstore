from django.shortcuts import render
from rest_framework.generics import*
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import *

from designations.serializers import *


class DropdownDesignationReadView(ListAPIView):
    queryset = Designations.objects.all()
    serializer_class = DesignationReadSerializer


