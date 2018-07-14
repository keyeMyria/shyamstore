from app_products.views import *
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('org_product_categories_edit/<appmaster_id>/', AppProductCategoriesEditView.as_view()),
    path('org_product_edit/<appmaster_id>/', AppProductsEditView.as_view()),

]