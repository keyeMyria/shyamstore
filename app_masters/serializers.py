from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_masters.models import *
from app_category.models import *
from users.serializers import *
from app_category.serializers import *
import datetime
from app_products.serializers import *
from drf_extra_fields.fields import Base64ImageField


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


class UpdateOwnerInfoAppMastersSerializer(ModelSerializer):
    class Meta:
        model = AppMasters
        fields =['id','owner_name', 'owner_designation','owner_pic','business_est_year','store_address','lat','long']

    def update(self, instance, validated_data):
        #print('validated_data::',validated_data)
        app_id = instance.id
        app_master_exi_data = AppMasters.objects.filter(pk=app_id)
        if app_master_exi_data:
            instance.owner_name = validated_data.get('owner_name', instance.business_name)
            instance.owner_designation = validated_data.get('owner_designation', instance.business_name)
            instance.owner_pic = validated_data.get('owner_pic', instance.owner_pic)
            instance.business_est_year=validated_data.get('business_est_year',instance.business_est_year)
            instance.store_address = validated_data.get('store_address', instance.store_address)
            instance.lat = validated_data.get('lat', instance.lat)
            instance.long = validated_data.get('long', instance.long)
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
        fields =['id','business_name','business_description','business_est_year','logo','category','app_url','user','app_product_categories', 'app_imgs','owner_name','owner_designation','owner_pic','store_address','lat','long','designation_details']


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

class EditAppLogoSerializer(ModelSerializer):
    logo = Base64ImageField()
    class Meta:
        model = AppMasters
        fields =['id','logo']
    def update(self, instance, validated_data):
        import os
        import datetime
        try:
            existing_logo ='./media/' +str(instance.logo)
            instance.logo = validated_data.get('logo',instance.logo)
            #instance.business_name = validated_data.get('business_name', instance.business_name)
            #instance.business_description = validated_data.get('business_description',instance.business_description)
            instance.modified_at = datetime.datetime.now()
            instance.save()
            # print(os.path.isfile(existing_logo))
            if validated_data.get('logo') and os.path.isfile(existing_logo):
                os.remove(existing_logo)
        except Exception as e:
            raise e
        return instance

class EditOwnerLogoSerializer(ModelSerializer):
    owner_pic = Base64ImageField()
    class Meta:
        model = AppMasters
        fields =['id','owner_pic']

    def update(self, instance, validated_data):
        import os
        import datetime
        try:
            #print('validated_data::',validated_data)
            existing_logo ='./media/' +str(instance.owner_pic)
            instance.owner_pic = validated_data.get('owner_pic',instance.owner_pic)
            instance.save()
            if validated_data.get('owner_pic') and os.path.isfile(existing_logo):
                os.remove(existing_logo)
        except Exception as e:
            raise e
        return instance

class EditOwnerLogoSerializer(ModelSerializer):
    owner_pic = Base64ImageField()

    class Meta:
        model = AppMasters
        fields = ['id', 'owner_pic']

    def update(self, instance, validated_data):
        import os
        import datetime
        try:
            # print('validated_data::',validated_data)
            existing_logo = './media/' + str(instance.owner_pic)
            instance.owner_pic = validated_data.get('owner_pic', instance.owner_pic)
            instance.save()
            if validated_data.get('owner_pic') and os.path.isfile(existing_logo):
                os.remove(existing_logo)
        except Exception as e:
            raise e
        return instance


class AppImgagesSerializerBase64(ModelSerializer):
    app_images = Base64ImageField()
    app_image_id = serializers.IntegerField(required=False)
    class Meta:
        model = AppImgages
        fields = ['id', 'appmaster', 'app_images','app_image_id']

    def create(self,validated_data):
        import os
        import datetime
        try:
            #print('self',self.instance.id)
            #print('validated_data',validated_data)
            get_app_image_id = validated_data.pop('app_image_id')
            if get_app_image_id:
                existing_images =''
                img_data = AppImgages.objects.filter(appmaster_id=validated_data.get('appmaster'), pk=get_app_image_id)
                #print('img_data::',img_data)
                for data in img_data:
                    existing_images = './media/' + str(data.app_images)
                img_data.delete()
                if validated_data.get('app_images') and os.path.isfile(existing_images):
                     os.remove(existing_images)
                return AppImgages.objects.create(appmaster=validated_data.get('appmaster'),
                                                 app_images=validated_data.get('app_images'))

            else:
                return AppImgages.objects.create(appmaster=validated_data.get('appmaster'),
                                      app_images=validated_data.get('app_images'))



        except Exception as e:
            raise e