"""shyamstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_category.urls')),
    path('', include('app_masters.urls')),
    path('', include('temp_app.urls')),
    path('', include('users.urls')),
    path('', include('customers.urls')),
    path('', include('app_products.urls')),
    path('', include('app_payment.urls')),
    path('', include('orders.urls')),
    path('', include('app_messenger.urls')),
	path('', include('designations.urls')),
    path('paytm/', include('paytm.urls')),
    path('', include('sms.urls')),
    path('messages/', include('chat.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
