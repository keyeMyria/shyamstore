from users import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    # path('create_user/',views.CreateUsersView.as_view())
    path('login/', views.CustomObtainAuthToken.as_view()),
    path('edit_step2_owner_details/<pk>/',views.EditStepTowOwnerDetailsView.as_view()),
    path('app_and_user_details/<pk>/', views.UserDetailsAndAppMasterDetailsView.as_view()),
    path('dropdown_designations/', views.DropdownDesignationReadView.as_view()),
    # path('edit_step2/<user_id>/', views.EditUserDetailsView.as_view()),
]