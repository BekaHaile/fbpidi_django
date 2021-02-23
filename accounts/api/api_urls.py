from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from accounts.api.api_views import CustomerSignUpView, exchange_token


urlpatterns = [
    path("login/", obtain_auth_token, name = "api_customer_login"),
    path("register/", CustomerSignUpView.as_view(), name = "api_customer_signup" ),
    
    #12345
    path('social/<str:backend>/', exchange_token, name="api_social"), #localhost:8000/client/accounts/social/facebook/
    
    # path("logout/", )


]