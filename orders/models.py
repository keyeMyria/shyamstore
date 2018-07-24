from django.db import models
from django.contrib.auth.models import *
from customers.models import Customers
from app_masters.models import AppMasters
from app_products.models import AppProducts
from uom.models import Currency

# Create your models here.
class Orders(models.Model):
    customer = models.ForeignKey(Customers,on_delete=models.CASCADE, related_name='customer_details')
    price = models.DecimalField(max_digits=20,decimal_places=2)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)
    def customer_details(self):
        data_dict = {}
        customer_details = Customers.objects.filter(pk=self.customer_id)
        for customer in customer_details:
            data_dict['id'] = customer.id
            data_dict['name'] = customer.customer_name
            data_dict['email'] = customer.email
            data_dict['contact_no'] = customer.contact_no
        return data_dict


class OrderDetails(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE, related_name='order_details', blank=True, null=True)
    appmaster = models.ForeignKey(AppMasters,on_delete=models.CASCADE)
    product =  models.ForeignKey(AppProducts,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    IGST = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    CGST = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    GST = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    packaging_cost = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    uom_currency = models.ForeignKey(Currency,on_delete=models.CASCADE, default=1, related_name="uom_currency")
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)