 

from django.urls import path,include
from accounts.views import CustomerSignUpView,CompleteLoginView,LoginView


urlpatterns = [
    path("register/",CustomerSignUpView.as_view(),name="register"),
    path("complete-auth/",CompleteLoginView.as_view(),name="complete_login"),
    path("accounts/",include("django.contrib.auth.urls")),
    path("api/",include("accounts.api.api_urls")),
    path('login_custom/', LoginView.as_view(), name='login_custom'),
    path('social-auth', include('social_django.urls', namespace='social_dj_auth')),
]