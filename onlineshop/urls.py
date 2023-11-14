"""
URL configuration for onlineshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from main import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,re_path,include

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    path('register', views.register),


    path('search', views.search),

    path('', views.homepage),
    path('categories', views.category),
    path('checkout', views.checkout),
    path('addtocheckout', views.addtocheckout),
    path('checkout/selectaddress', views.checkoutaddress),
    path('checkout/payment', views.payment),
    path('checkout/pay', views.pay),

    path('profile', views.profile),
    path('profile/address', views.addresses),
    path('profile/address/selectaddress', views.selectaddress),
    path('profile/address/editaddress/<str:addresspk>', views.editaddress),
    path('profile/editprofile', views.editprofile),


    path('product', views.product),
    path('product/<str:serialnumber>', views.product),
    path('product/<str:serialnumber>/leavecomment', views.product),
    path('leavecomment/<str:serialnumber>', views.leavecomment),

    path('productlist', views.productlist),
    path('productlist/<str:searchtype>/<str:keyword>', views.productlist),


    path('magazine/<str:name>', views.magazine),

    path('ckeditor/', include('ckeditor_uploader.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
