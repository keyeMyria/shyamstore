from users import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    # path('create_user/',views.CreateUsersView.as_view())
    path('login/', views.CustomObtainAuthToken.as_view()),


]