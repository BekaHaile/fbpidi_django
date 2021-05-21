from django.urls import path
         

from accounts.api.api_views import CompanyAdminSignUpView, CustomerSignUpView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [  
    path("login/", obtain_auth_token, name = "api_login"),
]
