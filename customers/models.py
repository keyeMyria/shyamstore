from django.db import models
from states.models import *
from app_masters.models import *
from django.contrib.auth.models import *
# from orders.models import *

class Customers(models.Model):
    customer_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    contact_no = models.CharField(max_length=15,default=None, blank=True, null=True)
    password = models.CharField(max_length=255)

    # class Meta:
    #     unique_together = ('email', 'contact_no',)

    def __str__(self):
        return str(self.customer_name)

    def app_master(self):
        app_master_list = []
        customer_mapping_data = CustomerAppMasterMapping.objects.filter(customer_id=self.id,is_active=True)
        for data in customer_mapping_data:
            app_master_list.append({
             "id":data.app_master.id,
             "business_name":data.app_master.business_name,
             "business_description": data.app_master.business_description,
             "logo": data.app_master.logo.url if data.app_master.logo else "",
             "locality": data.app_master.locality ,
             "category": data.app_master.category()
             })
        return app_master_list






class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    address = models.TextField()
    pincode = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.address)

class CustomerAppMasterMapping(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE,related_name="customer")
    app_master = models.ForeignKey(AppMasters,on_delete=models.CASCADE,related_name="app_master")
    referred_by = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # class Meta:
    #     unique_together = ('app_master', 'customer',)

    def __str__(self):
        return str(self.id)








