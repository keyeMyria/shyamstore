from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from orders import views

urlpatterns=[
    path('create_orders/', views.OrdersCreateView.as_view()),
    path('all_order_details/', views.OrdersDetailsReadView.as_view()),
    path('all_order_details/<pk>/', views.OrdersDetailsReadView.as_view()),
    path('cancel_orders/<pk>/', views.CancelOrderView.as_view()),
    path('cancel_by_orderdetails_id/<pk>/', views.CancelOrderByOrderDetailsIdView.as_view()),

    path('all_order_by_app_id/<appmaster_id>/', views.OrdersDetailsBYAppIdReadView.as_view()),
]