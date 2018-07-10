from django.db import models
from app_masters.models import *

# Create your models here.

class AppProductCategories(models.Model):
    app_master = models.ForeignKey(AppMasters, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class AppProducts(models.Model):
    STATUS_CHOICES = (
        ('1', 'hide'),
        ('0', 'None'),
    )
    app_master = models.ForeignKey(AppMasters,on_delete=models.CASCADE)
    product_category = models.ForeignKey(AppProductCategories,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    product_code = models.CharField(max_length=20, blank=True,null=True)
    price = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    discounted_price = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    tags = models.TextField(blank=True,null=True)
    hide_org_price_status = models.BooleanField(choices=STATUS_CHOICES, default=0)
    packing_charges = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product_name)

class ProductImages(models.Model):
    app_product = models.ForeignKey(AppProducts, on_delete=models.CASCADE)
    product_image = models.CharField(max_length=255, blank=True,null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)
