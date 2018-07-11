from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_category.serializers import *
from temp_app.models import *
from django.contrib.auth.models import *
from app_masters.models import *
from users.models import *

class TempAppCategoryMapingSerializer(ModelSerializer):
    class Meta:
        model = TempAppCategoryMapings
        fields =['id','appmaster','app_category']





class TempAppMastersCreateSerializer(ModelSerializer):

    session_id = serializers.CharField(required=False, max_length=50)
    app_category = serializers.IntegerField()

    class Meta:
        model = TempAppMasters
        fields =['id','session_id','app_category']

    def create(self, validated_data):
        session_id = validated_data.pop("session_id")
        temp_app = TempAppMasters.objects.create(session_id=session_id)
        if temp_app.id:
            TempAppCategoryMapings.objects.create(appmaster_id = temp_app.id, app_category_id = validated_data.get("app_category"))
        return {'id':temp_app.id,'session_id':session_id,'app_category':validated_data.get("app_category")}



class TempAppMastersDetailsSerializer(ModelSerializer):
    app_category = TempAppCategoryMapingSerializer(many=True)

    class Meta:
        model = TempAppMasters
        fields =['id','session_id', 'app_category']

class TempUsersAndStepTwoSerializer(ModelSerializer):
    # owner_pic = serializers.ImageField(max_length=None, use_url='users_pic')
    class Meta:
        model = TempUsers
        fields =['id','owner_name','session_id','owner_designation','owner_pic']
        # fields ="__all__"

    def create(self, validated_data):
        temp_user = TempUsers.objects.create(**validated_data)
        return temp_user

class TempAppImagesSerializer(ModelSerializer):
    app_images = serializers.ImageField(max_length=None, use_url='app_images')

    class Meta:
        model = TempAppImgs
        # fields =['id','app','app_images', 'src']
        fields =['id','app','app_images']

class TempAppMastersSerializer(ModelSerializer):
    class Meta:
        model = TempAppMasters
        fields =['id','session_id', 'business_name', 'business_description', 'logo', 'locality','is_physical', 'store_address','lat',
                 'long', 'contact_no1','contact_no2', 'contact_no3','is_always_open','created_at','is_active','app_url']

class BusinessLogoUploadAndStepOneSerializer(ModelSerializer):
    # logo = serializers.ImageField(max_length=None, use_url='logo')
    class Meta:
        model = TempAppMasters
        # fields =['id','logo','business_name','business_description','locality']
        fields =['id','logo','business_name','business_description']

class UpdateTempAppCategoryMappingSerializer(ModelSerializer):

    class Meta:
        model = TempAppCategoryMapings
        fields = ['appmaster','app_category']

    # def update(self, instance, validated_data):
    #     return validated_data


class UpdateTempAppCategoryMapingsSerializer(ModelSerializer):
    # appmaster = TempAppMastersSerializer(many=True)
    # app_category = TempAppCategoryMapingSerializer(many=True)
    class Meta:
        model = TempAppCategoryMapings
        fields =['id','appmaster','app_category']

    def update(self, instance, validated_data):
        print('validated_data::',validated_data)
        instance.app_category = validated_data.get("app_category",instance.app_category)
        instance.save()
        return instance


class UserRegistrationAndStepLastSerializer(ModelSerializer):
    class Meta:
        model = TempUsers
        fields =['id','email_id','contact_no']
    def update(self, instance, validated_data):
        instance.email_id = validated_data.get("email_id", instance.email_id)
        instance.contact_no = validated_data.get("contact_no", instance.contact_no)
        try:
            temp_user_data = TempUsers.objects.filter(id=instance.id)
            for user_data in temp_user_data:
                insert_user = User.objects.create(first_name = str(user_data.owner_name),username=validated_data.get("email_id"),email=validated_data.get("email_id"), is_staff = True, password = "123456")
                session_id = user_data.session_id
                user_id = insert_user.id
                insert_user_details = UserDetails.objects.create(contact_no=validated_data.get("contact_no"),
                                                                 users_pic = user_data.owner_pic,
                                                                 user_id = user_id)

                temp_app_data = TempAppMasters.objects.filter(session_id=session_id)[:1]
                # temp_app_data = TempAppMasters.objects.filter(session_id=session_id)
                print(temp_app_data)
            for app_data in temp_app_data:

                insert_app_master = AppMasters.objects.create(user_id=user_id,
                                                              business_name = app_data.business_name,
                                                              business_description=app_data.business_description,
                                                              logo=app_data.logo,
                                                              locality=app_data.locality,
                                                              app_url=app_data.app_url
                                                              )
                app_master_id = insert_app_master.id
                temp_app_master_id= app_data.id
                app_data.is_active = False
                app_data.save()
            if temp_app_master_id:
                temp_appmaping_data = TempAppCategoryMapings.objects.filter(appmaster_id=temp_app_master_id)[:1]
            # print('temp_appmaping_data::', temp_appmaping_data)
            for mapping_data in temp_appmaping_data:
                insert_app_mapping=AppCategoryMapings.objects.create(appmaster_id = app_master_id,app_category_id = mapping_data.app_category_id)
                app_category_mapping_id = insert_app_mapping.id

            temp_app_images_data = TempAppImgs.objects.filter(app_id = temp_app_master_id)[:1]
            print('temp_app_images_data::', temp_app_images_data)
            for app_img in temp_app_images_data:
                insert_app_images = AppImgages.objects.create(app = insert_app_master,app_images=app_img.app_images)

        except Exception as e:
            raise e
        finally:
            instance.save()
            return instance



class TempUsersDetailsSerializer(ModelSerializer):
    owner_pic = serializers.ImageField(max_length=None, use_url='users_pic')
    class Meta:
        model = TempUsers
        # fields =['id','owner_name','session_id','owner_designation','owner_pic']
        fields ="__all__"



class TempAppCategoryMapingDetailsSerializer(ModelSerializer):
    appmaster = TempAppMastersSerializer()
    app_category = AppCategoriesSerializer()
    # app_img = TempAppImagesSerializer()

    class Meta:
        model = TempAppCategoryMapings
        # fields =['id','appmaster','app_category']
        fields =['id','appmaster','app_category','app_imgs']

class InsertAppUrlTempAppMasterSerializer(ModelSerializer):
    class Meta:
        model = TempAppMasters
        fields =['id','app_url','locality']


class CreateTempAppProductCategoriesSerializer(ModelSerializer):
    class Meta:
        model = TempAppProductCategories
        fields =['id','app_master','category_name','description']

class CreateTempAppProductSerializer(ModelSerializer):
    class Meta:
        model = TempAppProducts
        fields =['id','app_master','product_category','product_name','description','product_code','price',
                 'discounted_price', 'tags', 'packing_charges', 'hide_org_price_status']


class CreateMultipleTempAppProductsSerializer(ModelSerializer):
    products = CreateTempAppProductSerializer(many =True)
    class Meta:
        model = TempAppProducts
        fields = ['products']
    def create(self, validated_data):
        data_list = []
        products =  validated_data['products']
        for data in products:
            product = dict(data)
            add_product = TempAppProducts.objects.create(**product)
            data_list.append(add_product)
        return {'products': data_list}









class CreateMultipleTempAppProductCategoriesSerializer(ModelSerializer):
    product_categories = CreateTempAppProductCategoriesSerializer(many=True)
    class Meta:
        model = TempAppProductCategories
        fields = ['product_categories']

    def create(self, validated_data):
        data_list = []
        print('validated_data::', validated_data['product_categories'])
        categoies =  validated_data['product_categories']
        for data in categoies:
            category = dict(data)
            add_category = TempAppProductCategories.objects.create(**category)
            data_list.append(add_category)
        return {'product_categories': data_list}
    def update(self, instance, validated_data):
        return validated_data



class TempAppProductCategoriesSerializer(ModelSerializer):
    class Meta:
        model = TempAppProductCategories
        fields ="__all__"


class TempAppProductSerializer(ModelSerializer):
    app_master = TempAppMastersSerializer()
    product_category = TempAppProductCategoriesSerializer()
    class Meta:
        model = TempAppProducts
        fields = "__all__"

class AddCategoryAndProductSerializer(ModelSerializer):
    product = CreateTempAppProductSerializer(many=True)
    product_category = TempAppProductCategoriesSerializer()

    class Meta:
        model = TempAppProducts
        fields = ['product_category','product']
        # fields = ['category_name', 'description', 'app_master','product']

    def create(self, validated_data):
        total_pro = []
        # print('validated_data::', validated_data)
        product_category_data = validated_data.get('product_category')
        product_list_data = validated_data.get('product')

        product_category = TempAppProductCategories.objects.create(**dict(product_category_data))
        if product_category.id:
            for product in list(product_list_data):
                # print(dict(product))
                add_product = TempAppProducts.objects.create(product_category = product_category, app_master = product_category.app_master , **dict(product))
                total_pro.append(add_product)


        return {'product_category':product_category,'product':total_pro}
        # return validated_data