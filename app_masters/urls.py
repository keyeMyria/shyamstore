from app_masters import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('upload_coverpic/',views.CoverPicsUpload.as_view()),
    path('org_app_master/<user_id>/',views.OrgAppMasterListView.as_view()),
    path('edit_org_app_master/<pk>/',views.EditOrgAppMasterView.as_view()),

    path('edit_org_app_mappings/<pk>/',views.EditOrgAppMappingsView.as_view()),
    path('edit_step1_app_master/<pk>/',views.EditStep1OrgAppMasterView.as_view()),

    path('edit_org_app_mappings/<appmaster_id>/',views.EditOrgAppMappingsView.as_view()),
    path('add_app_visiting_count/<pk>/',views.AddAppVisitingCountView.as_view()),
    path('most_viewed_app/',views.MostViewedAppReadView.as_view()),
    path('search_app/',views.SearchAppReadView.as_view()),
    path('update_usiness_url/<pk>/',views.UpdateBusinessUrlView.as_view()),
    path('app_all_details/<pk>/',views.AppAllDetailsByIdReadView.as_view()),
    path('insert_org_app_url/<pk>/',views.EditBusinessUrlView.as_view()),


]