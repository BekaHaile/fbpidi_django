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
import random
import string

from django.conf import settings
from django.conf.urls.static import static 

from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView

from admin_site.admin import admin_site

from accounts.views import activate,api_activate, activate_subscription
from accounts.profile_view import IndexView

def create_url_string():
    return ''.join(random.choices(string.ascii_letters + string.digits,k=100))

urlpatterns = [
    
    path("",IndexView.as_view(),name='index'),    
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('api_activate/<uidb64>/<token>/', api_activate, name = 'api_activate'),
    # path('activate_subscribtion/<subscribtion_id>/<token>/',activate_subscription,name = 'activate_subscribtion' ),
    path('activate_subscribtion/<uidb64>/<token>/',activate_subscription,name = 'activate_subscribtion' ),
    
    # third party app urls
    path('summernote/', include('django_summernote.urls')),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),



    ### web urls
    path("admin/",admin_site.urls),# admin page urls
    path("accounts/",include("accounts.urls")), 
    
    path("chat/", include('chat.urls')),
    path("collaborations/", include('collaborations.urls')),
    path('company/', include('company.urls')),
    path('product/', include('product.urls')),
    
    path('auth/oauth/', include('rest_framework_social_oauth2.urls')), ### For both web and rest api social auth,
    #  this is the redirect url for the web E.x. http://localhost:8000/auth/oauth/complete/google-oauth2/ 
    #  this is b/c the rest_framework_social_oauth2 embade the social_django in itself
    
    
    ### api urls
    path("api/", include("core.api.api_urls")), #urls for the mobile view
    path("api/accounts/", include("accounts.api.api_urls") ),# api login, logout ...
    path("api/collaborations/", include("collaborations.api.api_urls")),
    path('api/company/', include('company.api.api_urls')),
    path("api/chat/", include('chat.api.api_urls')),
    path('api/product/', include('product.api.api_urls')),
    path('report_builder/', include('report_builder.urls')),
    
    
    path("not_found/",TemplateView.as_view(template_name="frontpages/404.html"),name="not_found"),
    path("underconstruction/",TemplateView.as_view(template_name="frontpages/underconstruction.html"),name="underconstruction"),

    
]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)