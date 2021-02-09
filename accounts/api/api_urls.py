from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from .api_views import CustomerSignUpView


urlpatterns = [
    path("login/", obtain_auth_token, name = "api_customer_login"),
    path("register/", CustomerSignUpView.as_view(), name = "api_customer_signup" ),
    # path("logout/", )


]