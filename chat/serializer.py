from .models import ChatMessage, ChatGroup
from rest_framework import serializers


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ChatMessage()
        fields = ('id','content')
