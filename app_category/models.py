from django.db import models
from django.contrib.auth.models import *

# Create your models here.
class AppCategories(models.Model):
    category_name = models.CharField(max_length=100)
    category_code = models.CharField(max_length=10)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    app_count = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.category_name)

