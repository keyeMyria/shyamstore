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
    # owner_designation = serializers.IntegerField()
    # store_address = serializers.CharField(required=False)
    # lat = serializers.CharField(required=False)
    # long = serializers.CharField(required=False)
    # business_est_year = serializers.IntegerField(required=False)
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
        instance.save()
        return instance

    # def create(self, validated_data):
    #     session_id = validated_data.get("session_id")
    #     owner_designation_id = validated_data.pop('owner_designation')
    #     store_address = validated_data.pop('store_address')
    #     lat = validated_data.pop('lat')
    #     long = validated_data.pop('long')
    #     business_est_year = validated_data.pop('business_est_year')
    #     print('owner_designation_id::', owner_designation_id)
    #     user_exiest = TempUsers.objects.filter(session_id = session_id)
    #     if user_exiest:
    #         for user in user_exiest:
    #             user.owner_name = validated_data.get("owner_name",user.owner_name)
    #             user.owner_designation_id = owner_designation_id
    #             user.owner_pic = validated_data.get("owner_pic",user.owner_pic)
    #             user.save()
    #             user_id =user.id
    #     else:
    #         temp_user = TempUsers.objects.create(owner_designation_id = owner_designation_id,**validated_data)
    #         user_id = temp_user.id
    #     data_dict = {}
    #     temp_app_details = TempAppMasters.objects.filter(session_id=session_id)
    #     for app_data in temp_app_details:
    #         app_data.store_address = store_address
    #         app_data.lat = lat
    #         app_data.long = long
    #         app_data.business_est_year = business_est_year
    #         app_data.save()
    #         data_dict['store_address'] = app_data.store_address
    #         data_dict['lat'] = app_data.lat
    #         data_dict['long'] = app_data.long
    #         data_dict['business_est_year'] = app_data.business_est_year
    #
    #
    #
    #     user_details = TempUsers.objects.filter(pk=user_id,session_id=session_id)
    #     for user_data in user_details:
    #         data_dict['id']=user_data.id
    #         data_dict['owner_name']  =user_data.owner_name
    #         data_dict['session_id']=user_data.session_id
    #         data_dict['owner_designation']=user_data.owner_designation_id
    #         data_dict['owner_pic']=user_data.owner_pic
    #
    #     return data_dict

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

    class Meta:
        model = TempAppMasters
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
            # print('temp_user_id::',instance.id)
            user_id,session_id = self.insert_users(temp_user_id =instance.id,
                                                  email=validated_data.get("email_id"),
                                                  contact_no=validated_data.get("contact_no") )
            # print('user_id::',user_id)
            # print('session_id::',session_id)

            temp_app_data = TempAppMasters.objects.filter(session_id=session_id)[:1]
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
            self.insert_product_and_category(temp_app=temp_app_master_id, org_app=app_master_id)
            for mapping_data in temp_appmaping_data:
                insert_app_mapping=AppCategoryMapings.objects.create(appmaster_id = app_master_id,app_category_id = mapping_data.app_category_id)
                app_category_mapping_id = insert_app_mapping.id

            temp_app_images_data = TempAppImgs.objects.filter(app_id = temp_app_master_id)
            for app_img in temp_app_images_data:
                insert_app_images = AppImgages.objects.create(appmaster_id = app_master_id,app_images=app_img.app_images)




        except Exception as e:
            raise e
        finally:
            instance.save()
            return instance

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

    def insert_users(self, temp_user_id:int, email:str, contact_no:int):
        # print('temp_user fgrfg::',temp_user_id)
        try:
            temp_user_data = TempUsers.objects.filter(id=temp_user_id)
            for user in temp_user_data:
                session_id = user.session_id
                user_exiest = User.objects.filter(email=email)
                if user_exiest:
                    for org_user in user_exiest:
                        org_user.first_name = str(user.owner_name)
                        org_user.is_superuser = False
                        org_user.is_staff = False
                        org_user.set_password("123456")
                        org_user.save()
                        user_id = org_user.id
                    user_details_data = UserDetails.objects.filter(user_id=user_id)
                    for details in user_details_data:
                        details.contact_no = contact_no
                        details.users_pic = user.owner_pic
                        details.designation_id = user.owner_designation_id
                        details.save()
                else:
                    insert_user = User.objects.create(first_name=str(user.owner_name),
                                                      username=email,
                                                      email=email,
                                                      is_staff=False,
                                                      is_superuser=False,
                                                      is_active=True)
                    insert_user.set_password("123456")
                    insert_user.save()
                    user_id = insert_user.id
                    UserDetails.objects.create(contact_no=contact_no,
                                               users_pic=user.owner_pic,
                                               designation = user.owner_designation,
                                               user_id=user_id)

            return user_id, session_id
        except Exception as e:
            raise e

    def insert_App_Master(self,session_id,user_id):
        pass






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