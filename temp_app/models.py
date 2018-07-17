from django.db import models
from app_category.models import *
from django.conf import settings
from users.models import Designations



class TempAppCoverPhotos(models.Model):
    app_category = models.ForeignKey(AppCategories, on_delete=models.CASCADE)
    cover_pic = models.ImageField(upload_to="cover_pics", default=None)
    is_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class TempAppMasters(models.Model):
    STATUS_CHOICES = (
        ('1', 'is_allose_open'),
        ('0', 'None'),
    )

    session_id = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100, default=None, blank=True,null=True)
    business_description = models.TextField(blank=True,null=True)
    logo = models.ImageField(upload_to="logos", default=None, blank=True,null=True)
    locality = models.TextField(blank=True,null=True)
    is_physical = models.BooleanField(default=True)
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
    app_url = models.CharField(max_length=200, blank=True,null=False)
    def __str__(self):
        return str(self.id)
    # def app_imgs(self):
    #     return self.a

class TempAppCategoryMapings(models.Model):
    STATUS_CHOICES = (
        ('1', 'is_primary'),
        ('0', 'None'),
    )
    appmaster = models.ForeignKey(TempAppMasters, on_delete=models.CASCADE, related_name='appmaster_appmapping')
    app_category = models.ForeignKey(AppCategories, on_delete=models.CASCADE, related_name='app_category')
    is_primary = models.BooleanField(choices=STATUS_CHOICES,default=0)


    def __str__(self):
        return str(self.id)
    def app_imgs(self):
        img_list = []
        app_imgs = TempAppImgs.objects.filter(app_id=self.appmaster.id)
        for img_data in app_imgs:
            img_list.append({'id': img_data.id, 'app_master_id':img_data.app.id, 'app_img': img_data.app_images.url})
        return img_list
    def product_details(self):
        product_details =[]
        category_data = TempAppProductCategories.objects.filter(app_master_id=self.appmaster.id, is_active=True)
        for category in category_data:
            product_list = []
            category_dict = {}
            category_dict['id']=category.id
            category_dict['category_name'] = category.category_name
            category_dict['description'] = category.description

            product_data = TempAppProducts.objects.filter(app_master_id=self.appmaster.id,product_category_id=category_dict['id'],is_active=True)
            for product in product_data:
                products_dict = {}
                products_dict["id"]=product.id
                products_dict["product_category_id"]=product.product_category_id
                products_dict["product_name"]=product.product_name
                products_dict['description'] = product.description
                products_dict['product_code'] = product.product_code
                products_dict['price'] = product.price
                products_dict['discounted_price'] = product.discounted_price
                products_dict['tags'] = product.tags
                products_dict['hide_org_price_status'] = product.hide_org_price_status
                products_dict['packing_charges'] = product.packing_charges
                product_list.append(products_dict)

            category_dict["products"] = product_list

            product_details.append(category_dict)
        return product_details


class TempAppProductCategories(models.Model):
    app_master = models.ForeignKey(TempAppMasters, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('app_master', 'category_name',)

    def __str__(self):
        return str(self.id)

class TempAppProducts(models.Model):
    STATUS_CHOICES = (
        ('1', 'hide'),
        ('0', 'None'),
    )
    app_master = models.ForeignKey(TempAppMasters,on_delete=models.CASCADE, blank=True,null=True)
    product_category = models.ForeignKey(TempAppProductCategories,on_delete=models.CASCADE, blank=True,null=True)
    product_name = models.CharField(max_length=255, blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    product_code = models.CharField(max_length=20, blank=True,null=True)
    price = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    discounted_price = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    tags = models.TextField(blank=True,null=True)
    hide_org_price_status = models.BooleanField(choices=STATUS_CHOICES, default=0, blank=True,null=False)
    packing_charges = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product_name)

class TempProductImages(models.Model):
    app_product = models.ForeignKey(TempAppProducts, on_delete=models.CASCADE)
    product_image = models.CharField(max_length=255, blank=True,null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

class TempUsers(models.Model):
    owner_name = models.CharField(max_length=255)
    session_id = models.CharField(max_length=50)
    owner_designation = models.ForeignKey(Designations, on_delete=models.CASCADE,blank=True, null=True)
    owner_pic = models.ImageField(upload_to="users_pic", default=None, blank=True, null=True)
    email_id = models.EmailField(default=None,blank=True, null=True)
    contact_no = models.BigIntegerField(default=None,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner_name)

class TempAppImgs(models.Model):
    app = models.ForeignKey(TempAppMasters, on_delete=models.CASCADE)
    app_images = models.ImageField(upload_to='app_images', default=None)
    src = models.CharField(max_length=100, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
