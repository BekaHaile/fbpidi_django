from django.urls import path,include
from .views import Index

urlpatterns = [
    path("polls/", Index.as_view(), name = "polls_view" ),
]