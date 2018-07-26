from django.shortcuts import render
from temp_app.serializers import *
from rest_framework.generics import*
from rest_framework.views import *
from rest_framework import status, viewsets
from PIL import Image


class CreateTempAppMaster(CreateAPIView):
    queryset = TempAppMasters.objects.all()
    # serializer_class = TempAppMastersSerializer
    serializer_class = TempAppMastersCreateSerializer
    # def post(self, request, format=None):
    #     app_category_id = request.data[0].pop('app_category')
    #     temp_app_master = TempAppMasters.objects.create(**request.data[0])
    #     if temp_app_master:
    #         TempAppCategoryMapings.objects.create(appmaster_id = temp_app_master.id, app_category_id = app_category_id)
    #     return Response(request.data)



class TempAppMasterListView(ListAPIView):
    queryset = TempAppMasters.objects.all()
    serializer_class = TempAppMastersSerializer

class TempAppMasterListDetailBySessionView(ListAPIView):
    queryset = TempAppMasters.objects.all()
    serializer_class = TempAppMastersDetailsSerializer
    def get_queryset(self):
        session_id = self.kwargs['session']
        if session_id:
            queryset_data = TempAppMasters.objects.filter(session_id=session_id)

        return queryset_data



# class TempAppMasterDetailsByIDView(ListAPIView):
#     queryset = TempAppMasters.objects.all()
#     serializer_class = TempAppMastersSerializer
#     def get_queryset(self):
#         id = self.kwargs['pk']
#         if id:
#             queryset_data = TempAppMasters.objects.filter(id=id)
#         return queryset_data


class TempAppDetailsView(ListAPIView):
    queryset = TempAppCategoryMapings
    serializer_class = TempAppCategoryMapingDetailsSerializer
    def get_queryset(self):
    # def get(self, request):
        appmaster_id = self.kwargs['appmaster_id']
        queryset = TempAppCategoryMapings.objects.filter(appmaster_id=appmaster_id)

        # app_img = TempAppImgs.objects.filter(app_id=appmaster_id)
        # responce = {'mapping_data':queryset, 'app_img':app_img}
        return queryset
        # return Response(responce)


class BusinessLogoUploadAndStepOneView(RetrieveUpdateAPIView):
    queryset = TempAppMasters.objects.all()
    serializer_class = BusinessLogoUploadAndStepOneSerializer


class CreateTempUsersAndStepTwoView(ListCreateAPIView):
    # queryset = TempUsers.objects.all()
    serializer_class = TempUsersAndStepTwoSerializer
    def get_queryset(self):
        session_id = self.kwargs['session']
        return TempAppMasters.objects.filter(session_id=session_id)

class TempUsersDetailView(ListAPIView):
    queryset = TempUsers.objects.all()
    serializer_class = TempUsersDetailsSerializer
    def get_queryset(self):
        session_id = self.kwargs['session']
        queryset = TempUsers.objects.filter(session_id=session_id)
        return queryset

class CreateListTempAppImgs(ListCreateAPIView):
    queryset = TempAppImgs.objects.all()
    serializer_class = TempAppImagesSerializer
    # serializer_class = MultipleUploadImagesSerializer


class MultipleUploadImgAndStepThreeView(ListCreateAPIView):
    queryset = TempAppImgs.objects.all()
    serializer_class = TempAppImagesSerializer




class UpdateTempAppCategoryMapingsById(RetrieveUpdateAPIView):
    queryset = TempAppCategoryMapings.objects.all()
    serializer_class = UpdateTempAppCategoryMapingsSerializer



class CategoryMapingsUpdate(UpdateAPIView):
    queryset = TempAppCategoryMapings.objects.all()
    serializer_class = UpdateTempAppCategoryMappingSerializer
    def update(self, request, *args, **kwargs):
        appmaster_id = kwargs['pk']
        temp_mapping_data = TempAppCategoryMapings.objects.filter(appmaster_id=appmaster_id)[:1]
        for data in temp_mapping_data:
            data.app_category_id = request.data['app_category']
            data.save()

        return Response({'app_category':request.data['app_category'], 'appmaster':appmaster_id})






class UserRegistrationAndStepLastView(RetrieveUpdateAPIView):
    queryset = TempAppMasters.objects.all()
    serializer_class = UserRegistrationAndStepLastSerializer




class InsertAppUrlTempAppMasterView(RetrieveUpdateAPIView):
    queryset = TempAppMasters.objects.all()
    serializer_class = InsertAppUrlTempAppMasterSerializer

class CreateTempAppProductCategoriesView(ListCreateAPIView):
    queryset = TempAppProductCategories.objects.all()
    #serializer_class = CreateTempAppProductCategoriesSerializer
    serializer_class = CreateMultipleTempAppProductCategoriesSerializer


class CreateTempAppProductView(ListCreateAPIView):
    queryset = TempAppProducts.objects.all()
    # serializer_class = CreateTempAppProductSerializer
    serializer_class = CreateMultipleTempAppProductsSerializer

class TempAppProductListView(ListAPIView):
    queryset = TempAppProducts.objects.all()
    serializer_class = TempAppProductSerializer

class TempAppProductByIdView(ListAPIView):
    queryset = TempAppProducts.objects.all()
    serializer_class = TempAppProductSerializer
    def get_queryset(self):
        id = self.kwargs['pk']
        return TempAppProducts.objects.filter(pk=id)

class SearchTempAppProductByCategoryView(ListAPIView):
    queryset = TempAppProducts.objects.all()
    serializer_class = TempAppProductSerializer
    def get_queryset(self):
        categort_id = self.kwargs['categort_id']
        return TempAppProducts.objects.filter(product_category_id=categort_id)

class EditTempAppProductCategoriesView(RetrieveUpdateAPIView):
    queryset = TempAppProductCategories.objects.all()
    serializer_class = CreateTempAppProductCategoriesSerializer


class AddCategoryAndProductView(ListCreateAPIView):
    queryset = TempAppProductCategories.objects.all()
    serializer_class = AddCategoryAndProductSerializer

class CreateMultiTempAppProductCategoriesView(CreateAPIView):
    queryset = TempAppProducts.objects.all()
    serializer_class = CreateMultipleTempAppProductCategoriesSerializer


class EditTempAppProductCategoriesView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        appmaster_id = self.kwargs['appmaster_id']
        get_datas = TempAppProductCategories.objects.filter(app_master_id=appmaster_id, is_active = True)
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
            pro_cat_data = TempAppProductCategories.objects.filter(id__in=del_ids)
            for del_data in pro_cat_data:
                del_data.is_active = False
                del_data.save()

        for data in request.data["product_categories"]:
            if data["id"] in upd_ids:
                pro_cat_data = TempAppProductCategories.objects.filter(pk=data["id"])
                for update_data in pro_cat_data:
                    update_data.category_name = data["category_name"]
                    update_data.description = data["description"]
                    update_data.save()
            else:
                TempAppProductCategories.objects.create(app_master_id = data["app_master"],
                                                        category_name = data["category_name"],
                                                        description = data["description"])
        categories = TempAppProductCategories.objects.filter(is_active = True,app_master_id=appmaster_id)
        data_list =[]
        for data in categories:
            product_list = []
            product_data = TempAppProducts.objects.filter(product_category_id=data.id ,is_active=True)
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


        return Response({"product_categories": data_list})

class EditTempAppProductsView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        appmaster_id = self.kwargs['appmaster_id']
        # print("appmaster_id:", appmaster_id)
        exiest_ids = []
        for data in request.data["products"]:
            get_datas = TempAppProducts.objects.filter(app_master_id=appmaster_id,
                                                       product_category_id=data["product_category"],
                                                       is_active = True)
            for ids in get_datas:
                exiest_ids.append(ids.id)
        upd_ids =[]
        del_ids =[]
        # print('exiest_ids::', exiest_ids)
        if exiest_ids:
            for product in request.data["products"]:
                if product["id"]:
                    upd_ids.append(product["id"])
                    del_ids = list(set(exiest_ids)-set(upd_ids))
        # print('del_ids::', del_ids)

        if del_ids:
            print('upd_ids:{}\ndel_ids:{}'.format(upd_ids, del_ids))
            product_data = TempAppProducts.objects.filter(id__in=del_ids)
            for del_data in product_data:
                del_data.is_active = False
                del_data.save()
        for data in request.data["products"]:
            if data["id"] in upd_ids:
                pro_data = TempAppProducts.objects.filter(pk=data["id"])
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
                TempAppProducts.objects.create(app_master_id=app_master_id,
                    product_category_id=product_category_id, **data)
        products = TempAppProducts.objects.filter(is_active = True,app_master_id=appmaster_id)
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


