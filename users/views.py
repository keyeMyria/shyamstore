from django.shortcuts import render
from users.serializers import *
from rest_framework.generics import*
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import *
# Create your views here.

# class CreateUsersView(CreateAPIView):
#     queryset = UserDetails.objects.all()
#     serializer_class = UsersSerializer

class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response=super(CustomObtainAuthToken,self).post(request,*args,**kwargs)
        print('response.data::::',response.data)
        token=Token.objects.get(key=response.data['token'])
        user=User.objects.get(id=token.user_id)
        serializer=UserLoginSerializer(user,many=True)

        if user:
            data_dict = {
                'token': token.key,
                'user_id': user.pk,
                'username':user.username,
                'email': user.email
            }
            if user.is_staff:
                data_dict['user_role']="staff"
            if user.is_superuser:
                data_dict['user_role'] = "admin"


            return Response(data_dict)
        else:
            return Response({'message':'Invalid Login','status':status.HTTP_400_BAD_REQUEST})



class EditStep2OwnerDetailsView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    print('queryset::',queryset)
    serializer = EditStep2OwnerDetailsSerializer

class UserDetailsAndAppMasterDetailsView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersAppDetailsSerializer

