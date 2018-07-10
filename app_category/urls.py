from app_category import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('all_categories/',views.CategoriesListReadView.as_view()),
    path('all_categories/<pk>/',views.CategoryByIdReadView.as_view())


]