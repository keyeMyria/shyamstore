from django.shortcuts import render
from app_masters.serializers import *
from rest_framework.generics import*
from app_category.serializers import *

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

class EditOrgAppMappingsView(RetrieveUpdateAPIView):
    queryset = AppCategoryMapings.objects.all()
    serializer_class = UpdateOrgAppMappingsSerializer
    def get_queryset(self):
        appmaster_id = self.kwargs['appmaster_id']
        print('appmaster_id::', appmaster_id)
        queryset = AppCategoryMapings.objects.filter(appmaster_id=appmaster_id)
        return queryset

