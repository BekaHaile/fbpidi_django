from .models import ChatMessage, ChatGroup
from rest_framework import serializers
from datetime import datetime


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField('get_sender_name')
    sender_image = serializers.SerializerMethodField('get_sender_image')
    time = serializers.SerializerMethodField('get_time')
    chat_group = serializers.SerializerMethodField('get_chat_group')
    sender_status = serializers.SerializerMethodField('get_sender_status')
    
    class Meta:
        model  = ChatMessage()
        fields = ('id','content', 'sender_name', 'sender_image', 'time','read', 'chat_group', 'sender_status')
   
    def get_sender_name(self,chatmessage):
        return chatmessage.sender.username
   
    def get_sender_status(self, chatmessage):
        sender = chatmessage.sender
        chat_group = chatmessage.chat_group
        if sender in chat_group.connected_users.all():
            return 'online'
        else:
            return 'offline'
    
    def get_time(self, chatmessage):
        str_date_time = datetime.strftime(chatmessage.timestamp , "%y/%m/%d %H:%M:%S")
        parsed_str_date_time = datetime.strptime(str_date_time, '%y/%m/%d %H:%M:%S') 
        return str_date_time
    
    def get_chat_group(self, chatmessage):
        return chatmessage.chat_group.group_name
        
    def get_sender_image(self, chatmessage):
        
        if chatmessage.sender.profile_image:
            return chatmessage.sender.profile_image.url
        else:
            if chatmessage.sender.is_staff:
                return chatmessage.sender.get_company().get_image()
            else:
                return '/static/frontpages/images/clients/unkonwn_user_icon.png'
                # frontpages\images\clients

    
       
