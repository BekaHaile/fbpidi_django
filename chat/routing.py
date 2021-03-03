from django.urls import re_path, path

from . import consumers


websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    path('ws/chat/<str:group_name>/', consumers.ChatConsumer.as_asgi()), #called from templates/admin/chat/chat_layout.html and template/frontpage/chat/chat.html
    path('ws/unread_messages/', consumers.CheckUnreadMessages.as_asgi()) #called from templates/admin/partials/header.html
]