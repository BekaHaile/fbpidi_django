 

from django.urls import path,include
from accounts.views import CustomerSignUpView,CompleteLoginView,LoginView, Subscribe
from accounts.profile_view import *
appname = "accounts"
urlpatterns = [
    path("register/",CustomerSignUpView.as_view(),name="register"),
    path("subscribe/", Subscribe, name="subscribe"),
    path("unsubscribe/",Subscribe, name="unsubscribe"),
    path("user-login/",LoginView.as_view(),name="cm_login"),
    path("complete-auth/",CompleteLoginView.as_view(),name="complete_login"),
    path('social-auth', include('social_django.urls', namespace='socail')), # if restframework_social_auth is also,
    path("",include("django.contrib.auth.urls")),
    path("mydash/",ProfileView.as_view(),name="mydash"),
    path("myfavorite/",MyFavorite.as_view(),name="favorite"),
    path("orders/",MyOrders.as_view(),name="orders"),

    
]