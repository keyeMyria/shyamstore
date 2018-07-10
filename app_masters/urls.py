from app_masters import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('upload_coverpic/',views.CoverPicsUpload.as_view()),
    path('org_app_master/<user_id>/',views.OrgAppMasterListView.as_view()),
    path('edit_org_app_master/<pk>/',views.EditOrgAppMasterView.as_view()),
    path('edit_org_app_mappings/<appmaster_id>/',views.EditOrgAppMappingsView.as_view())


]