from django.db import models
from django.contrib.auth.models import *

class Currency(models.Model):
    currency = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return str(self.id)