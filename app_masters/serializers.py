from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_masters.models import *
from app_category.models import *
from users.serializers import *
from app_category.serializers import *
import datetime
from app_products.serializers import *


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
        fields =['id','logo', 'category', 'business_name','created_at','locality','user']
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
    class Meta:
        model = AppCategoryMapings
        fields = ['appmaster','app_category']

class AddAppMasterImagesSerializer(ModelSerializer):
    app_images = serializers.ImageField(max_length=None, use_url='app_images')
    class Meta:
        model = AppImgages
        fields = ["id", "app", "app_images","created_at"]


class UpdateStep1OrgAppMastersSerializer(ModelSerializer):
    logo = serializers.ImageField(max_length=None, use_url='logo',required=False) #define the type of field
    user_id = serializers.IntegerField() #define the type of field
    app_master_images = AddAppMasterImagesSerializer(many=True) # add the serializer for the foreignkey model
    #print('app_master_images::',app_master_images)
    class Meta:
        model = AppMasters
        fields =['id','logo', 'business_name','modified_at','user_id','app_master_images']

    def update(self, instance, validated_data):
        print('validated_data::',validated_data)
        app_images_data = validated_data.pop('app_master_images')
        user_id = validated_data.get('user_id')
        app_id = instance.id
        #print('user_id::',user_id)
        #print('app_id::', app_id)
        app_master_exi_data = AppMasters.objects.filter(user_id=user_id,pk=app_id)
        #print('app_master_exi_data:::',app_master_exi_data)
        if app_master_exi_data:

            instance.business_name=validated_data.get('business_name',instance.business_name)
            instance.logo = validated_data.get('logo', instance.logo)
            instance.modified_at = datetime.datetime.now()
            instance.save()
        return instance


class AddAppVisitingCountSerializer(ModelSerializer):
    class Meta:
        model = AppMasters
        fields = ["id", "visiting_count"]

    def update(self, instance, validated_data):
        instance.visiting_count = instance.visiting_count + 1
        instance.save()
        return instance


class SearchAppMastersSerializer(ModelSerializer):
    logo = serializers.ImageField(max_length=None, use_url='logo')
    user = UserSerializer()
    class Meta:
        model = AppMasters
        fields =['id','logo', 'category', 'business_name','created_at','locality','user']

class UpdateBusinessUrlSerializer(ModelSerializer):
    class Meta:
        model = AppMasters
        fields =['id','app_url']

class AppAllDetailsSerializer(ModelSerializer):
    # user = UserSerializer()
    user = UserAndUserDetailsSerializer()
    app_product_categories = AppProductCategorySerializer(many=True)
    # app_images = AddAppMasterImagesSerializer(many=True)
    class Meta:
        model = AppMasters
        fields =['id','business_name','business_description','business_est_year','logo','category','app_url','user','app_product_categories', 'app_imgs']


class EditBusinessUrlSerializer(ModelSerializer):
    class Meta:
        model = AppMasters
        fields =['id','app_url']

class AppImgagesSerializer(ModelSerializer):
    app_images = serializers.ImageField(max_length=None, use_url='app_images')
    class Meta:
        model = AppImgages
        fields = ['id', 'appmaster', 'app_images']



class EditAppLogoAndNameSerializer(ModelSerializer):
    class Meta:
        model = AppMasters
        fields =['id','logo', 'business_name','business_description']
    def update(self, instance, validated_data):
        import os
        import datetime
        try:
            existing_logo ='./media/' +str(instance.logo)
            instance.logo = validated_data.get('logo',instance.logo)
            instance.business_name = validated_data.get('business_name', instance.business_name)
            instance.business_description = validated_data.get('business_description',instance.business_description)
            instance.modified_at = datetime.datetime.now()

            instance.save()
            # print(os.path.isfile(existing_logo))
            if validated_data.get('logo') and os.path.isfile(existing_logo):
                os.remove(existing_logo)
        except Exception as e:
            raise e
        return instance