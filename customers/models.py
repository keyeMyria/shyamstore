from django.db import models
from states.models import *

class Customers(models.Model):
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField()
    contact_no = models.BigIntegerField(default=None, blank=True, null=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return str(self.customer_name)


class customer_address(models.Model):
    customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    address = models.TextField()
    pincode = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.address)

