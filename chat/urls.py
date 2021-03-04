from django.urls import include, path
from .views import index, room, chat_with, ChatList

urlpatterns = [
    path('', index, name = "chat"),
    path('with/<str:reciever_name>/', chat_with, name= "chat_with"),
    path('<str:requested_group_name>/', room, name = "chat_room"),
    path('customer_chat_list/', ChatList.as_view(), name = "customer_chat_list" ),
    
    
]