from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_category.models import *

class CategoriesListSerializer(ModelSerializer):
    class Meta:
        model = AppCategories
        fields =['id','category_name','category_code','description','created_at','is_deleted','app_count','created_by_id','status']

class AppCategoriesSerializer(ModelSerializer):
    class Meta:
        model = AppCategories
        fields = "__all__"