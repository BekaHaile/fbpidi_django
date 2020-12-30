"""fbpims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static 

from django.contrib import admin
from django.urls import path,include,re_path

from accounts.views import (CustomerAdminSignUpView,UserListView,RolesView,UserLogView,
                        UserDetailView,profileImage,CreateUserView,GroupView)
from admin_site.admin import admin_site


urlpatterns = [
    # admin page urls
    path("admin/",admin_site.urls),
    # frontpage urls 
    path("",include("core.urls")),
    # third party app urls
    path('summernote/', include('django_summernote.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)