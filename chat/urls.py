from django.urls import include, path
from .views import index, room, chat_with, ChatList

urlpatterns = [
    path('with/<str:reciever_name>/', chat_with, name= "chat_with"),
    path('customer_chat_list/', ChatList.as_view(), name = "customer_chat_list" ),
    path('<str:requested_group_name>/', room, name = "chat_room"),
    
    
    
]