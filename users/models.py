from django.db import models
from states.models import *
from django.contrib.auth.models import *
from app_masters.models import *


class Designations(models.Model):
    designation_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class Roles(models.Model):
    role_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.role_name)

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_details')
    users_pic = models.ImageField(upload_to="users_pic", default=None)
    contact_no = models.BigIntegerField()
    address = models.TextField(blank=True,null=True)
    state = models.ForeignKey(States, on_delete=models.CASCADE,blank=True,null=True)
    city = models.CharField(max_length=100, blank=True,null=True)
    pincode = models.CharField(max_length=10, blank=True,null=True)
    current_status = models.BooleanField(default=True)
    login_by_IP = models.CharField(max_length=20, blank=True,null=True)
    designation = models.ForeignKey(Designations, on_delete=models.SET_NULL, blank=True,null=True)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, blank=True,null=True)
    wellcome_msg = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    # parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent')

    def __str__(self):
        return str(self.id)

    def app_details(self):
        app_details = []
        app_data = AppMasters.objects.filter(user_id=self.user_id)
        for app in app_data:
            data_dict = {"id":app.id,
                         "app_name":app.business_name,
                         "app_description":app.business_description,
                         "logo":app.logo.url}
            app_details.append(data_dict)
        print('app_details::', app_details)
        return app_details




