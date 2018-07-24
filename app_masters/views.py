from django.shortcuts import render
from app_masters.serializers import *
from rest_framework.generics import*
from app_category.serializers import *
from rest_framework.views import *
from rest_framework import status, viewsets
from PIL import Image
from users.models import *
from rest_framework import filters
from django.conf import settings
import os

class CoverPicsUpload(ListCreateAPIView):
    queryset = AppMasters.objects.all()
    serializer_class = CoverImgUploadSerializer

class OrgAppMasterListView(ListAPIView):
    queryset = AppMasters.objects.all()
    serializer_class = OrgAppMastersSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        self.queryset = AppMasters.objects.filter(user_id=user_id)
        return self.queryset

class EditOrgAppMasterView(RetrieveUpdateAPIView):
    queryset = AppMasters.objects.all()
    serializer_class = UpdateOrgAppMastersSerializer

class EditOrgAppMappingsView(UpdateAPIView):
    queryset = AppCategoryMapings.objects.all()
    serializer_class = UpdateOrgAppMappingsSerializer
    def update(self, request, *args, **kwargs):
        appmaster_id = kwargs['pk']
        temp_mapping_data = AppCategoryMapings.objects.filter(appmaster_id=appmaster_id)[:1]
        for data in temp_mapping_data:
            data.app_category_id = request.data['app_category']
            data.save()
        return Response({'app_category':request.data['app_category'], 'appmaster':appmaster_id})

class EditStep1OrgAppMasterView(RetrieveUpdateAPIView):
    queryset = AppMasters.objects.all()
    serializer_class = UpdateStep1OrgAppMastersSerializer

class AddAppVisitingCountView(RetrieveUpdateAPIView):
    queryset = AppMasters.objects.all()
    serializer_class =AddAppVisitingCountSerializer

class MostViewedAppReadView(ListAPIView):
    queryset = AppMasters.objects.filter(is_active = True).order_by("-visiting_count")
    serializer_class = OrgAppMastersSerializer

class SearchAppReadView(ListAPIView):
    queryset = AppMasters.objects.filter(is_active=True)
    serializer_class = SearchAppMastersSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('locality','business_name')
    def get_queryset(self):
        queryset = AppMasters.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        if latitude and longitude:
            print("latitude:{} and longitude:{}".format(latitude,longitude))
        if category:
            if category.find(",") > 0:
                category_ids = category.split(",")
                category_ids = [int(id) for id in category_ids]
            else:
                category_ids = [category]

            category_mapping_data = AppCategoryMapings.objects.filter(app_category__in=category_ids)
            app_master_ids = [data.appmaster_id for data in category_mapping_data]
            queryset = AppMasters.objects.filter(id__in = app_master_ids,is_active = True)



        return queryset

class UpdateBusinessUrlView(RetrieveUpdateAPIView):
    queryset = AppMasters.objects.all()
    serializer_class = UpdateBusinessUrlSerializer

class AppAllDetailsByIdReadView(RetrieveAPIView):
    queryset = AppMasters.objects.all()
    serializer_class = AppAllDetailsSerializer

class EditBusinessUrlView(RetrieveUpdateAPIView):
    queryset = AppMasters.objects.all()
    serializer_class = EditBusinessUrlSerializer


class MultipleImgUploadView(ListCreateAPIView):
    queryset = AppImgages.objects.all()
    serializer_class = AppImgagesSerializer

class EditAppLogoAndNameView(RetrieveUpdateAPIView):
    queryset = AppMasters.objects.all()
    serializer_class = EditAppLogoAndNameSerializer

class DeleteAppImageDelView(RetrieveUpdateDestroyAPIView):
    queryset = AppImgages.objects.all()
    serializer_class = AppImgagesSerializer
    def delete(self, request, *args, **kwargs):
        base_url = "/".join(request.build_absolute_uri().split("/")[:3])+settings.MEDIA_URL
        id = self.kwargs['pk']
        img_data = AppImgages.objects.filter(pk=id)
        for data in img_data:
            app_master_id = data.appmaster.id
            existing_img = './media/' + str(data.app_images)
        img_data.delete()

        # print('request.build_absolute_uri::',base_url)
        if os.path.isfile(existing_img):
            os.remove(existing_img)
        responce_list = []
        rest_imgs = AppImgages.objects.filter(appmaster_id=app_master_id)
        for details in rest_imgs:
            responce_dict = {"id":details.id,"appmaster":details.appmaster.id,"app_images":base_url+str(details.app_images)}
            responce_list.append(responce_dict)

        return Response(responce_list)


