from django.contrib import admin
from temp_app.models import *

admin.site.register(TempAppMasters)
admin.site.register(TempAppProductCategories)
admin.site.register(TempAppCoverPhotos)
admin.site.register(TempAppProducts)
admin.site.register(TempAppCategoryMapings)

# Register your models here.
