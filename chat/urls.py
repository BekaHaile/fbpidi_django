from django.urls import include, path
from .views import index, room

urlpatterns = [
    path('', index, name = "chat"),
    path('<str:group_name>/', room, name = "chat_room"),
]