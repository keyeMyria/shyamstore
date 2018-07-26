from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from designations.views import *

urlpatterns=[
    path('dropdown_designations/', DropdownDesignationReadView.as_view()),
]