from django.db import models


# Create your models here.

class Countries(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.country_name)

class States(models.Model):
    state_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=100)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.state_name)



