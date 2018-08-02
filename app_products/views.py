from django.shortcuts import render
from app_products.models import *
from app_products.serializers import *
from rest_framework.views import *
from rest_framework.generics import*

class AppProductCategoriesByAppMasterEditView(RetrieveUpdateAPIView):

    def update(self, request, *args, **kwargs):
        print('rupam')
        appmaster_id = self.kwargs['appmaster_id']
        get_datas = AppProductCategories.objects.filter(app_master_id=appmaster_id, is_active = True)
        exiest_ids = [ids.id for ids in get_datas]
        upd_ids =[]
        del_ids =[]
        print('exiest_ids::', exiest_ids)
        for category in request.data["product_categories"]:
            if category["id"] and exiest_ids:
                upd_ids.append(category["id"])
                del_ids = list(set(exiest_ids)-set(upd_ids))


        if del_ids:
            print('upd_ids:{}\ndel_ids:{}'.format(upd_ids, del_ids))
            pro_cat_data = AppProductCategories.objects.filter(id__in=del_ids)
            for del_data in pro_cat_data:
                del_data.is_active = False
                del_data.save()


        for data in request.data["product_categories"]:
            if data["id"] in upd_ids:
                pro_cat_data = AppProductCategories.objects.filter(pk=data["id"])
                for update_data in pro_cat_data:
                    update_data.category_name = data["category_name"]
                    update_data.description = data["description"]
                    update_data.save()
            else:
                AppProductCategories.objects.create(app_master_id = data["app_master"],
                                                        category_name = data["category_name"],
                                                        description = data["description"])
        categories = AppProductCategories.objects.filter(is_active = True,app_master_id=appmaster_id)
        data_list =[]
        for data in categories:
            product_list = []
            product_data = AppProducts.objects.filter(product_category_id=data.id ,is_active=True)
            for product in product_data:
                product_dict = {"id":product.id,
                                "product_name":product.product_name,
                                "price":product.price,
                                "discounted_price":product.discounted_price,
                                "tags":product.tags,
                                "packing_charges":product.packing_charges}
                product_list.append(product_dict)

            data_dict = {"id":data.id,"category_name":data.category_name, "description":data.description,"products":product_list}
            data_list.append(data_dict)
            print('data_list::',data_list)

        return Response({"product_categories": data_list})

    # def get(self, request, *args, **kwargs):
    #     appmaster_id = self.kwargs['appmaster_id']
    #     query = AppProductCategories.objects.filter(app_master_id=appmaster_id, is_active=True)

class AppProductsEditView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        appmaster_id = self.kwargs['appmaster_id']

        exiest_ids = []
        for data in request.data["products"]:

            get_datas = AppProducts.objects.filter(app_master_id=appmaster_id,
                                                       product_category_id=data["product_category"],
                                                       is_active = True)

            for ids in get_datas:
                exiest_ids.append(ids.id)
        upd_ids =[]
        del_ids =[]
        print('exiest_ids::', exiest_ids)
        if exiest_ids:
            for product in request.data["products"]:
                if product["id"]:
                    upd_ids.append(product["id"])
                    del_ids = list(set(exiest_ids)-set(upd_ids))
        # print('del_ids::', del_ids)

        if del_ids:
            print('upd_ids:{}\ndel_ids:{}'.format(upd_ids, del_ids))
            product_data = AppProducts.objects.filter(id__in=del_ids)
            for del_data in product_data:
                del_data.is_active = False
                del_data.save()
        for data in request.data["products"]:
            if data["id"] in upd_ids:
                pro_data = AppProducts.objects.filter(pk=data["id"])
                for update_data in pro_data:
                    update_data.app_master_id=data["app_master"]
                    update_data.product_category_id=data["product_category"]
                    update_data.product_name=data["product_name"]
                    # update_data.description=data["description"]
                    # update_data.product_code=data["product_code"]
                    update_data.price=data["price"]
                    update_data.discounted_price=data["discounted_price"]
                    update_data.tags=data["tags"]
                    update_data.packing_charges=data["packing_charges"]
                    # update_data.hide_org_price_status=data["hide_org_price_status"]
                    update_data.save()
            else:
                app_master_id = data.pop("app_master")
                product_category_id = data.pop("product_category")
                AppProducts.objects.create(app_master_id=app_master_id,
                    product_category_id=product_category_id, **data)
        products = AppProducts.objects.filter(is_active = True,app_master_id=appmaster_id)
        data_list =[]
        for pro_data in products:
            data_dict ={}
            data_dict['id'] = pro_data.id
            data_dict['app_master'] = pro_data.app_master_id
            data_dict['product_category'] = pro_data.product_category_id
            data_dict['product_name'] = pro_data.product_name
            data_dict['description'] = pro_data.description
            data_dict['product_code'] = pro_data.product_code
            data_dict['price'] = pro_data.price
            data_dict['discounted_price'] = pro_data.discounted_price
            data_dict['tags'] = pro_data.tags
            data_dict['packing_charges'] = pro_data.packing_charges
            data_dict['hide_org_price_status'] = pro_data.hide_org_price_status
            data_list.append(data_dict)


        return Response({"products": data_list})
        # return Response(request.data)

class EditAppProductsView(RetrieveUpdateAPIView):
    queryset = AppProducts.objects.filter(is_active = True)
    serializer_class = AppProductsSerializer

class DeleteAppProductsView(RetrieveUpdateAPIView):
    queryset = AppProducts.objects.filter(is_active = True)
    serializer_class = DeleteAppProductsSerializer

class AddAppProductCreateView(ListCreateAPIView):
    queryset = AppProducts.objects.filter(is_active=True)
    serializer_class = AppProductsSerializer

class AppProductCategoriesCreateView(ListCreateAPIView):
    queryset = AppProductCategories.objects.all()
    serializer_class = ProductCategorySerializer

class AppProductCategoriesEditView(RetrieveUpdateAPIView):
    queryset = AppProductCategories.objects.all()
    serializer_class = ProductCategorySerializer

class AppProductCategoriesDeleteView(RetrieveUpdateAPIView):
    queryset = AppProductCategories.objects.all()
    serializer_class = ProductCategoryDeleteSerializer

class AppProductAndCategoriesReadView(RetrieveAPIView):
    queryset = AppProductCategories.objects.all()
    serializer_class = AppProductCategorySerializer




