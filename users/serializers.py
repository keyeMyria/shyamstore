from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import *
from django.contrib.auth.models import *
from app_masters.serializers import *


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',

        ]

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields="__all__"

# class UsersDetailsSerializer(ModelSerializer):
#     users_pic = serializers.ImageField(max_length=None, use_url='users_pic')
#
#     class Meta:
#         model = UserDetails
#         fields =['id','users_pic','designation']
#
#
#
# class UsersSerializer(ModelSerializer):
#     # user_details = UsersDetailsSerializer(many=True)
#     class Meta:
#         model = User
#         fields =['id','username']
#
#     def create(self, validated_data):
#         user_username = validated_data.get("username")
#         # user_users_pic = validated_data.get("users_pic")
#         print('user_username::', user_username)
#         return True


class EditStep2OwnerDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id'
            'first_name',
            'email',

        ]


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id','users_pic','contact_no','app_details']


class UsersAppDetailsSerializer(ModelSerializer):
    # app_details = OrgAppMastersSerializer(many=True)
    user_details = UserDetailsSerializer(many=True)
    class Meta:
        model = User
        fields=["id","first_name","last_name","email","user_details"]

