from app_products.views import *
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path

urlpatterns = [
    path('org_product_categories_edit/<appmaster_id>/', AppProductCategoriesEditView.as_view()),
    path('org_product_edit/<appmaster_id>/', AppProductsEditView.as_view()),
    path('edit_app_products/<pk>/', EditAppProductsView.as_view()),#get product and update product
    path('delete_app_products/<pk>/', DeleteAppProductsView.as_view()),#delete product
    path('create_app_products/', AddAppProductCreateView.as_view()),#add product
    path('create_app_products_category/', AppProductCategoriesCreateView.as_view()),#add Categories
    path('edit_app_products_category/<pk>/', AppProductCategoriesEditView.as_view()),#edit Categories
    path('delete_app_products_category/<pk>/', AppProductCategoriesDeleteView.as_view()),#Delete Categories
    path('app_products&category_details/<pk>/', AppProductAndCategoriesReadView.as_view()),#Categories and product details

]