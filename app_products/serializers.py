from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_products.models import *

class AppProductCategorySerializer(ModelSerializer):
    class Meta:
        model = AppProductCategories
        fields =['id','category_name','description','products']