from django.urls import path, include
from core.api.api_views import ApiIndexView



urlpatterns = [

    path("home/", ApiIndexView.as_view(), name = "client_home"),
    path("accounts/", include("accounts.api.api_urls"), name = "client_account" ),# api login, logout ...
    path("collaborations/", include("collaborations.api.api_urls"), name = "client_collaborations"),
    

]