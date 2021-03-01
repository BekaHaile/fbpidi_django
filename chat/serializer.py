from .models import ChatMessage, ChatGroup
from rest_framework import serializers


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField('get_sender_name')
    sender_image = serializers.SerializerMethodField('get_sender_image')
    class Meta:
        model  = ChatMessage()
        fields = ('id','content', 'sender_name', 'sender_image', 'timestamp')
    def get_sender_name(self,chatmessage):
        return chatmessage.sender.username
    def get_sender_image(self, chatmessage):
        return chatmessage.sender.profile_image.url if chatmessage.sender.profile_image else None
