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

class UsersDetailsSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields =['id','users_pic','designation']
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




class EditStepTowOwnerDetailsSerializer(ModelSerializer):
    app_master_id = serializers.IntegerField()
    business_est_year = serializers.IntegerField()
    designation = serializers.CharField()
    users_pic = serializers.ImageField(max_length=None, use_url='media/users_pic')
    class Meta:
        model = User
        fields = ['id','first_name','designation','business_est_year','users_pic','app_master_id']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.save()
        user_id = instance.id
        user_details_data = UserDetails.objects.filter(user_id=user_id)[:1]
        for data in user_details_data:
            data.designation = validated_data.get("designation", data.designation)
            data.users_pic = validated_data.get("users_pic", data.users_pic)
            data.save()
            deg = data.designation
            pic = data.users_pic
        app_master_details = AppMasters.objects.filter(id=validated_data.get("app_master_id"))[:1]
        for app_data in app_master_details:
            app_data.business_est_year = validated_data.get("business_est_year", app_data.business_est_year)
            app_data.save()
            app_id =app_data.id
            est = app_data.business_est_year
        return {'id':user_id,
                'first_name':instance.first_name,
                'designation':deg,
                'business_est_year':est,
                'users_pic':pic,
                'app_master_id':app_id}


class UserDetailsAndAppDetailsSerializer(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id','users_pic','contact_no','app_details']


class UsersAppDetailsSerializer(ModelSerializer):
    user_details = UserDetailsAndAppDetailsSerializer(many=True)
    class Meta:
        model = User
        fields=["id","first_name","last_name","email","user_details"]

