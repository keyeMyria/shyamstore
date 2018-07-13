from django.shortcuts import render
from app_masters.serializers import *
from rest_framework.generics import*
from app_category.serializers import *
from rest_framework.views import *
from rest_framework import status, viewsets
from PIL import Image
from users.models import *

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
    queryset = AppMasters.objects.all().order_by("-visiting_count")
    serializer_class = OrgAppMastersSerializer
