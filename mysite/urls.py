"""
URL configuration for mysite project.

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
from django.urls import path, include,re_path

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from master_app.views import media_access


from django_otp.admin import OTPAdminSite


if settings.ENABLE_OTP:
    admin.site.__class__ = OTPAdminSite


admin.site.site_header  =  "You Shity Ass"  
admin.site.site_title  =  "You Shity Ass"
admin.site.index_title  =  "You Shity Ass"

urlpatterns = [
    path('chpoen/', admin.site.urls),
    path("", include("master_app.urls")),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('robots.txt', TemplateView.as_view(template_name="master_app/robots.txt", content_type='text/plain')),
    re_path(r'^media/(?P<path>.*)', media_access, name='media'),

]



if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    # urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
