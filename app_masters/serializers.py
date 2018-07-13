from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_masters.models import *
from app_category.models import *
from users.serializers import *
from app_category.serializers import *
import datetime


class CoverImgUploadSerializer(ModelSerializer):
    cover_pic = serializers.ImageField(max_length=None, use_url='cover_pics')

    class Meta:
        model = AppCoverPhotos
        fields =['id','app_category','cover_pic', 'is_admin', 'created_at', 'is_deleted']

class OrgAppCategoryMapingSerializer(ModelSerializer):
    class Meta:
        model = AppCategoryMapings
        fields =['id','appmaster','app_category']


class OrgAppMastersSerializer(ModelSerializer):
    logo = serializers.ImageField(max_length=None, use_url='logo')
    user = UserSerializer()
    class Meta:
        model = AppMasters
        fields =['id','logo', 'business_name','created_at','user']
        # fields ="__all__"



class UpdateOrgAppMastersSerializer(ModelSerializer):
    logo = serializers.ImageField(max_length=None, use_url='logo')

    class Meta:
        model = AppMasters
        fields =['id','logo', 'business_name','business_description','store_address']
    def update(self, instance, validated_data):
        instance.business_name = validated_data.get("business_name",instance.business_name)
        instance.business_description = validated_data.get("business_description",instance.business_description)
        instance.store_address = validated_data.get("store_address",instance.store_address)
        instance.logo = validated_data.get("logo",instance.logo)
        instance.save()
        return instance

class UpdateOrgAppMappingsSerializer(ModelSerializer):
    appmaster = OrgAppMastersSerializer()
    app_category = AppCategoriesSerializer()
    class Meta:
        model = AppCategoryMapings
        fields = ["id","appmaster","app_category"]

class AddAppVisitingCountSerializer(ModelSerializer):
    class Meta:
        model = AppMasters
        fields = ["id", "visiting_count"]

    def update(self, instance, validated_data):
        instance.visiting_count = instance.visiting_count + 1
        instance.save()
        return instance



