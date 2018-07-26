from django.db import models
from django.contrib.auth.models import *

class Designations(models.Model):
    designation_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

