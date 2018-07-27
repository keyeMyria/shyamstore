from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import *
from designations.models import *


class DesignationReadSerializer(ModelSerializer):

    class Meta:
        model = Designations
        fields=["id","designation_name","status"]