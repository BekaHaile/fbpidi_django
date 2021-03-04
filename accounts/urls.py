 

from django.urls import path,include
from accounts.views import CustomerSignUpView,CompleteLoginView,LoginView

appname = "accounts"
urlpatterns = [
    path("register/",CustomerSignUpView.as_view(),name="register"),
    path("complete-auth/",CompleteLoginView.as_view(),name="complete_login"),
    path('social-auth', include('social_django.urls', namespace='socail')), # if restframework_social_auth is also,
    path("",include("django.contrib.auth.urls")),
    
]