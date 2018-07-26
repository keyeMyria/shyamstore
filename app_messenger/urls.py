from app_messenger import views
from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path


urlpatterns = [
    path('chats/', views.ChatSessionView.as_view()),
    # path('chats/<uri>/', views.ChatSessionView.as_view()),
    path('chats/<uri>/messages/', views.ChatSessionMessageView.as_view()),
    path('chat_members_details/', views.ChatSessionMemberListView.as_view()),
]
