from django.db import models
from django.contrib.auth.models import *
from app_masters.models import AppMasters
# Create your models here.

class AppMessenger(models.Model):
    sender_id =models.IntegerField()
    sender_type =models.CharField(max_length=100,blank=True,null=True)
    message=models.CharField(max_length=1000,blank=True,null=True)
    receiver_id=models.IntegerField()
    receiver_type=models.CharField(max_length=100,blank=True,null=True)
    app_id=models.ForeignKey(AppMasters,on_delete=models.CASCADE,blank=True,null=True)
    sending_time=models.DateTimeField(auto_now_add=True)
    receiving_time=models.DateTimeField(blank=True,null=True)
    view_time=models.DateTimeField(blank=True,null=True)
    msg_session = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return str(self.id)
