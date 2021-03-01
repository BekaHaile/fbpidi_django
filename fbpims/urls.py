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


from admin_site.admin import admin_site

from accounts.views import activate
from core.views import IndexView, ProfileView

urlpatterns = [
    
   
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    # third party app urls
    path('summernote/', include('django_summernote.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),



    ### web urls
    path("", include('core.urls') ), #has index url and other non-app related templates
    path("mydash/",ProfileView.as_view(),name="mydash"),

    
    path("admin/",admin_site.urls),# admin page urls
    path("accounts/",include("accounts.urls")), 
    path("chat/", include('chat.urls')),
    path("collaborations/", include('collaborations.urls')),
    path('company/', include('company.urls')),
    path('product/', include('product.urls')),
    
    
    ### api urls
    path('api/auth/oauth/', include('rest_framework_social_oauth2.urls')), ### for social auth
    path("api/", include("core.api.api_urls")), #urls for the mobile view
    path("api/accounts/", include("accounts.api.api_urls") ),# api login, logout ...
    path("api/collaborations/", include("collaborations.api.api_urls")),
    path('api/company/', include('company.api.api_urls')),
    path('api/product/', include('product.api.api_urls')),
    
    
    
    
]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)