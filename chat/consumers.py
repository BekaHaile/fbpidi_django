import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatGroup, ChatMessage
from .serializer import ChatMessageSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from accounts.models import User

class ChatConsumer(WebsocketConsumer):
    
    def new_message(self, data):
        sender = User.objects.get(username = data['from'])
        chat_group = ChatGroup.objects.get(group_name=self.group_name)
        new_message = ChatMessage(chat_group=chat_group, sender = sender, content = data['message'])
        new_message.save()
        result =[ChatMessageSerializer(new_message).data]
        self.send_chat_message(  result, "new_message")
        

    def fectch_messages(self, data):
        self.previous_messages = ChatMessageSerializer( ChatMessage.last_n_messages(self.group_name), many = True).data
        print("previous messages ", self.previous_messages)
        self.send_message(self.previous_messages)
        
    commands = {
            'fetch_messages': fectch_messages, 
            'new_message' : new_message
        }    

    def connect(self):
        
        requested_group = self.scope['url_route']['kwargs']['group_name']
        self.group_name = ""
        self.previous_messages = []
        try:
            group = get_object_or_404(ChatGroup, group_name = requested_group)
            self.group_name = group.group_name
        except Http404:
            group = ChatGroup(group_name=requested_group)
            group.save()
            self.group_name = group.group_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )        

        self.accept()
        
        print("Channel name is ", self.channel_name)
        

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket, then decide what to do depending on incoming command
    def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']
        print("from receive method command is ", command)
        self.commands[command](self, data)
        
    #accepts message and sends it
    def send_chat_message(self, message, command):
        # Send message to  a group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'command':command
               
            }
        )
    
    def send_message(self, message):
        self.send(text_data = json.dumps({'message':message}))    

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
           
        }))