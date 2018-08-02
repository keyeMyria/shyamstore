from django.db import models
from django.contrib.auth.models import *
from app_category.models import *
from designations.models import Designations
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
    business_est_year = models.IntegerField(blank=True,null=True)
    logo = models.ImageField(upload_to="logos", default=None, blank=True, null=True)
    locality = models.TextField(blank=True,null=True)
    is_physical_store = models.BooleanField(default=True)
    store_address = models.TextField(blank=True,null=True)
    lat = models.CharField(max_length=255, blank=True,null=True)
    long = models.CharField(max_length=255, blank=True, null=True)
    contact_no1 = models.BigIntegerField(blank=True,null=True)
    contact_no2 = models.BigIntegerField(blank=True,null=True)
    contact_no3 = models.BigIntegerField(blank=True,null=True)
    is_always_open = models.BooleanField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    app_url = models.CharField(max_length=500, blank=True, null=True)
    visiting_count = models.BigIntegerField(default=0, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    owner_designation = models.ForeignKey(Designations, on_delete=models.CASCADE, blank=True, null=True)
    owner_pic = models.ImageField(upload_to="owners_pic", default=None, blank=True, null=True)
    def __str__(self):
        return str(self.id)

    def category(self):
        category_dict = {}
        app_category_data = AppCategoryMapings.objects.filter(appmaster_id=self.id)
        for data in app_category_data:
            category_dict['category'] = data.app_category.category_name
        return category_dict['category']
    def app_imgs(self):
        app_img_list =[]
        get_img_data = AppImgages.objects.filter(appmaster_id=self.id)
        for data in get_img_data:
            app_img_list.append({'id':data.id,'app_master_id':data.appmaster.id, 'app_img':data.app_images.url})
        return app_img_list

    def designation_details(self):
        designation_details_dict = {}
        get_designation_data = Designations.objects.filter(pk=self.owner_designation_id)
        for data in get_designation_data:
            designation_details_dict['id'] = data.id
            designation_details_dict['designation_name'] = data.designation_name
        return designation_details_dict




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
    appmaster = models.ForeignKey(AppMasters, on_delete=models.CASCADE)
    app_images = models.ImageField(upload_to='app_images', default=None)
    src = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)