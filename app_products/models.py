from django.db import models
from app_masters.models import *

# Create your models here.

class AppProductCategories(models.Model):
    app_master = models.ForeignKey(AppMasters, on_delete=models.CASCADE,related_name="app_product_categories")
    category_name = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    def products(self):
        products_list = []
        data_dict = {}
        product_details = AppProducts.objects.filter(product_category_id=self.id,is_active=True)
        for data in product_details:
            data_dict['id'] = data.id
            data_dict['app_master'] = data.app_master_id
            data_dict['product_name'] = data.product_name
            data_dict['description'] = data.description
            data_dict['product_code'] = data.product_code
            data_dict['price'] = data.price
            data_dict['discounted_price'] = data.discounted_price
            data_dict['tags'] = data.tags
            data_dict['packing_charges'] = data.packing_charges
            data_dict['hide_org_price_status'] = data.hide_org_price_status
            products_list.append(data_dict)
        return products_list

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
