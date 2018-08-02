from users import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    # path('create_user/',views.CreateUsersView.as_view())
    path('login/', views.CustomObtainAuthToken.as_view()),
    path('edit_step2_owner_details/<pk>/',views.EditStepTowOwnerDetailsView.as_view()),
    path('app_and_user_details/<pk>/', views.UserDetailsAndAppMasterDetailsView.as_view()),

    path('app_user_list_by_frid/<franchise_id>/', views.UserListByFranchiseIDView.as_view()),
    path('otp_confirmation/<pk>/', views.UserActiveView.as_view())
]