from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_products.models import *
from datetime import datetime

class AppProductCategorySerializer(ModelSerializer):
    class Meta:
        model = AppProductCategories
        fields =['id','category_name','description','products']


class AppProductsSerializer(ModelSerializer):
    class Meta:
        model = AppProducts
        fields ="__all__"

    def update(self, instance, validated_data):
        instance.modified_at = datetime.now()
        instance.product_name=validated_data.get('product_name',instance.product_name)
        instance.description=validated_data.get('description',instance.description)
        instance.price=validated_data.get('price',instance.price)
        instance.discounted_price=validated_data.get('discounted_price',instance.discounted_price)
        instance.packing_charges=validated_data.get('packing_charges',instance.packing_charges)
        instance.product_category=validated_data.get('product_category',instance.product_category)
        instance.app_master=validated_data.get('app_master',instance.app_master)
        instance.save()
        return instance




class DeleteAppProductsSerializer(ModelSerializer):
    class Meta:
        model = AppProducts
        fields =['id','is_active']

    def update(self, instance, validated_data):
        instance.is_active = False
        instance.save()
        return instance

class ProductCategorySerializer(ModelSerializer):

    class Meta:
        model = AppProductCategories
        fields =['id','category_name','description','app_master']

class ProductCategoryDeleteSerializer(ModelSerializer):
    class Meta:
        model = AppProductCategories
        fields =['id','is_active']
    def update(self, instance, validated_data):
        instance.is_active = False
        instance.save()
        product_details = AppProducts.objects.filter(product_category_id= instance.id,is_active = True)
        for data in product_details:
            data.is_active = False
            data.save()
        return instance
