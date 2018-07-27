from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from app_category.serializers import *
from temp_app.models import *
from django.contrib.auth.models import *
from app_masters.models import *
from users.models import *
from app_products.models import *
# from passlib.hash import pbkdf2_sha256
from django.contrib.auth.models import User,Group
from rest_framework.exceptions import APIException # for define custom exception message

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
            TempAppCategoryMapings.objects.create(appmaster_id = temp_app.id,
                                                  app_category_id = validated_data.get("app_category"))
        return {'id':temp_app.id,'session_id':session_id,'app_category':validated_data.get("app_category")}



class TempAppMastersDetailsSerializer(ModelSerializer):
    app_category = TempAppCategoryMapingSerializer(many=True)

    class Meta:
        model = TempAppMasters
        fields =['id','session_id', 'app_category']

class TempUsersAndStepTwoSerializer(ModelSerializer):
    class Meta:
        model = TempAppMasters
        fields =['id','owner_name','owner_designation','owner_pic','store_address','lat','long','business_est_year']

    def update(self, instance, validated_data):
        instance.owner_name = validated_data.get('owner_name',instance.owner_name)
        instance.owner_designation = validated_data.get('owner_designation',instance.owner_designation)
        instance.owner_pic = validated_data.get('owner_pic',instance.owner_pic)
        instance.store_address = validated_data.get('store_address',instance.store_address)
        instance.lat = validated_data.get('lat',instance.lat)
        instance.long = validated_data.get('long',instance.long)
        instance.business_est_year = validated_data.get('business_est_year',instance.business_est_year)
        instance.is_active = True
        instance.save()
        return instance



class TempAppImagesSerializer(ModelSerializer):
    app_images = serializers.ImageField(max_length=None, use_url='app_images')

    class Meta:
        model = TempAppImgs
        fields =['id','app','app_images']

class TempAppMastersSerializer(ModelSerializer):
    class Meta:
        model = TempAppMasters
        fields =['id','session_id', 'business_name', 'business_description', 'logo', 'locality','is_physical', 'store_address','lat',
                 'long', 'contact_no1','contact_no2', 'contact_no3','is_always_open','created_at','is_active','app_url']

class BusinessLogoUploadAndStepOneSerializer(ModelSerializer):

    class Meta:
        model = TempAppMasters
        fields =['id','logo','business_name','business_description']

class UpdateTempAppCategoryMappingSerializer(ModelSerializer):

    class Meta:
        model = TempAppCategoryMapings
        fields = ['appmaster','app_category']


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
    email_id = serializers.EmailField(required=False)
    contact_no = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255,required=False)
    class Meta:
        model = TempAppMasters
        fields =['id','email_id','contact_no','name']
    def update(self, instance, validated_data):
        email_id = validated_data.pop("email_id")
        contact_no = validated_data.pop("contact_no")
        name = validated_data.pop("name")
        try:
            # print('temp_user_id::',instance.id)
            get_user_data = UserDetails.objects.filter(user__email=email_id, contact_no=contact_no)
            if not get_user_data:
                from nameparser import HumanName
                name = HumanName(name)
                temp_app_data = TempAppMasters.objects.filter(pk=instance.id)
                for app_data in temp_app_data:
                    insert_user = User.objects.create(first_name=str(name.first), last_name = str(name.last),
                                                      username=email_id,
                                                      email=email_id,
                                                      is_staff=False,
                                                      is_superuser=False,
                                                      is_active=True)
                    insert_user.set_password("123456")
                    insert_user.save()
                    user_id = insert_user.id
                    UserDetails.objects.create(contact_no=contact_no,
                                               user_id=user_id)

                    insert_app_master = AppMasters.objects.create(user_id=user_id,
                                                                  business_name = app_data.business_name,
                                                                  business_description=app_data.business_description,
                                                                  logo=app_data.logo,
                                                                  locality=app_data.locality,
                                                                  app_url=app_data.app_url,
                                                                  store_address = app_data.store_address,
                                                                  lat = app_data.lat,
                                                                  long = app_data.long,
                                                                  owner_name = app_data.owner_name,
                                                                  owner_designation = app_data.owner_designation,
                                                                  owner_pic = app_data.owner_pic,
                                                                  business_est_year = app_data.business_est_year
                                                                  )
                    app_master_id = insert_app_master.id
                    temp_app_master_id= app_data.id
                    app_data.is_active = False
                    app_data.save()
                if temp_app_master_id:
                    temp_appmaping_data = TempAppCategoryMapings.objects.filter(appmaster_id=temp_app_master_id)[:1]
                # print('temp_appmaping_data::', temp_appmaping_data)
                self.insert_product_and_category(temp_app=temp_app_master_id, org_app=app_master_id)
                for mapping_data in temp_appmaping_data:
                    insert_app_mapping=AppCategoryMapings.objects.create(appmaster_id = app_master_id,app_category_id = mapping_data.app_category_id)
                    app_category_mapping_id = insert_app_mapping.id

                temp_app_images_data = TempAppImgs.objects.filter(app_id = temp_app_master_id)
                for app_img in temp_app_images_data:
                    insert_app_images = AppImgages.objects.create(appmaster_id = app_master_id,app_images=app_img.app_images)
                return instance




        except Exception as e:
            # from rest_framework.response import Response
            # raise APIException({
            #     'msg': 'Please Login',
            #     'success': 0
            # })
            raise e



    def insert_product_and_category(self, temp_app:int,org_app:int):
        print('temp_app:',temp_app)
        print('org_app:',org_app)
        try:
            data_list = []
            temp_product_category_data = TempAppProductCategories.objects.filter(app_master_id=temp_app, is_active=True)
            print('temp_product_category_data:',temp_product_category_data)
            for category_data in temp_product_category_data:
                product_list = []
                org_category = AppProductCategories.objects.create(app_master_id =org_app,
                                                    category_name=category_data.category_name,
                                                    description=category_data.description)
                org_category_id = org_category.id
                temp_product_data = TempAppProducts.objects.filter(app_master_id=temp_app,
                                                                  product_category_id=category_data.id,
                                                                  is_active=True)
                print('org_category::',org_category)
                print('temp_product_data::',temp_product_data)
                for product in temp_product_data:
                    pro_dict = {}
                    org_app_master_id=org_app
                    pro_dict['product_name'] = product.product_name
                    pro_dict['description'] = product.description
                    pro_dict['product_code'] = product.product_code
                    pro_dict['price'] = product.price
                    pro_dict['discounted_price'] = product.discounted_price
                    pro_dict['tags'] = product.tags
                    pro_dict['hide_org_price_status'] = product.hide_org_price_status
                    pro_dict['packing_charges'] = product.packing_charges
                    org_product = AppProducts.objects.create(app_master_id=org_app_master_id,product_category_id =org_category_id,**pro_dict)
                    product_list.append(org_product.id)

                data_list.append({"categories_id":org_category_id,"products_ids":product_list})
            return data_list
        except Exception as e:
            raise e










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
        fields =['id','appmaster','app_category','app_imgs','product_details']

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