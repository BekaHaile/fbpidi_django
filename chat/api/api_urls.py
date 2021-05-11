from django.urls import include, path
from chat.api.api_views import  chat_ajax_handler, chat_with, CustomerChatList, check_username, list_unread_messages

urlpatterns = [
    path('', chat_ajax_handler.as_view(), name = "api_chat_request"),
    path('list_unread/',list_unread_messages.as_view(), name = "api_list_unread_messages"),
    path('with/', chat_with.as_view(), name= "api_chat_with"),
    path('chat_list/', CustomerChatList.as_view(), name = "api_chat_list" ),
    path('check_user/', check_username.as_view(), name ="api_check_chat_username"),
      
]