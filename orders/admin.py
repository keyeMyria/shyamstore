from django.contrib import admin
from orders.models import *

# Register your models her
admin.site.register(Orders)
admin.site.register(OrderDetails)
