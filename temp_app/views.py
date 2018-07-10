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


class CreateTempUsersAndStepTwoView(CreateAPIView):
    queryset = TempUsers.objects.all()
    serializer_class = TempUsersAndStepTwoSerializer

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
    queryset = TempUsers.objects.all()
    serializer_class = UserRegistrationAndStepLastSerializer

class InsertAppUrlTempAppMasterView(RetrieveUpdateAPIView):
    queryset = TempAppMasters.objects.all()
    serializer_class = InsertAppUrlTempAppMasterSerializer

class CreateTempAppProductCategoriesView(ListCreateAPIView):
    queryset = TempAppProductCategories.objects.all()
    serializer_class = CreateTempAppProductCategoriesSerializer



class CreateTempAppProductView(ListCreateAPIView):
    queryset = TempAppProducts.objects.all()
    serializer_class = CreateTempAppProductSerializer

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

