from app_payment import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


urlpatterns = [
    path('all_product_price_details/',views.AllProductPriceDetailsReadView.as_view())

]