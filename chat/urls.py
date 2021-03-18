from django.urls import include, path
from .views import  chat_ajax_handler, chat_with, CustomerChatList, check_username, list_unread_messages

urlpatterns = [
    path('',list_unread_messages, name = "list_unread_messages"),
    path('<int:id>/', chat_ajax_handler, name = "chat_request"),
    path('with/<str:reciever_name>/', chat_with, name= "chat_with"),
    path('customer_chat_list/', CustomerChatList.as_view(), name = "customer_chat_list" ),
    path('check_user/<str:username>/', check_username, name ="check_chat_username"),
      
]