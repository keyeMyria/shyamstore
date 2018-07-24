from app_messenger import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


urlpatterns = [
    path('app_messenger/',views.AppMessengerCreateView.as_view()),
    path('view_time/',views.AppMessengerManageView.as_view())
]
