from django.db import models
from django.contrib.auth.models import *

class AppPayment(models.Model):
    price = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)
    product_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product_name)
