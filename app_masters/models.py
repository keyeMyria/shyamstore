from django.db import models
from django.contrib.auth.models import *
from app_category.models import *

# Create your models here.

class AppCoverPhotos(models.Model):
    app_category = models.ForeignKey(AppCategories, on_delete=models.CASCADE)
    cover_pic = models.ImageField(upload_to="cover_pics", default=None)
    is_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class AppMasters(models.Model):
    STATUS_CHOICES = (
        ('1', 'is_allose_open'),
        ('0', 'None'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100, blank=True,null=True)
    business_description = models.TextField(blank=True, null=True)
    # logo = models.CharField(max_length=255, blank=True,null=True)
    logo = models.ImageField(upload_to="logos", default=None, blank=True, null=True)
    locality = models.TextField(blank=True,null=True)
    is_physical = models.BooleanField(default=True)
    store_address = models.TextField(blank=True,null=True)
    lat = models.CharField(max_length=255, blank=True,null=True)
    long = models.CharField(max_length=255, blank=True, null=True)
    contact_no1 = models.BigIntegerField(blank=True,null=True)
    contact_no2 = models.BigIntegerField(blank=True,null=True)
    contact_no3 = models.BigIntegerField(blank=True,null=True)
    is_allose_open = models.BooleanField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    app_url = models.CharField(max_length=500, blank=True, null=True)
    visiting_count = models.BigIntegerField(default=0, blank=True, null=True)
    def __str__(self):
        return str(self.id)


class AppCategoryMapings(models.Model):
    STATUS_CHOICES = (
        ('1', 'is_primary'),
        ('0', 'None'),
    )
    appmaster = models.ForeignKey(AppMasters, on_delete=models.CASCADE)
    app_category = models.ForeignKey(AppCategories, on_delete=models.CASCADE)
    is_primary = models.BooleanField(choices=STATUS_CHOICES,default=0)


    def __str__(self):
        return str(self.id)

class AppImgages(models.Model):
    app = models.ForeignKey(AppMasters, on_delete=models.CASCADE)
    app_images = models.ImageField(upload_to='app_images', default=None)
    src = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)