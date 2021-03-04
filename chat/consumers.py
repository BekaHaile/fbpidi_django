import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatGroup, ChatMessage
from .serializer import ChatMessageSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from accounts.models import User
from chat.views import get_unread_grouped_messages
from chat.models import ChatMessage

class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        sender = User.objects.get(username = data['from'])

        chat_group = list(ChatGroup.objects.ChatGroup.objects.get_or_create(group_name=self.group_name))
        chat_group = chat_group[0]
        new_message = ChatMessage(chat_group=chat_group, sender = sender, content = data['message'])
        if chat_group.count_connected_users() > 1: # if number of connected users is greater than 1, means the reciever is online. So, read = True 
            new_message.read = True
        new_message.save()
        result =[ChatMessageSerializer(new_message).data]
        self.send_chat_message(  result, "new_message")

    def fectch_messages(self, data):
        self.previous_messages = ChatMessageSerializer( ChatMessage.last_n_messages(self.group_name), many = True).data
        self.send_message(self.previous_messages)

    commands = {
            'fetch_messages': fectch_messages, 
            'new_message' : new_message
        }    

    #custom method for closing connection while exceptions occur
    def force_disconnect(self):
        self.send(text_data = json.dumps({'message':"Force Disconnect"}))
        
    
    def connect(self):
        
        requested_group = self.scope['url_route']['kwargs']['group_name']
        self.group_name = "" 
        self.previous_messages = []
        try:
            #get_or_create returns (ChatGroup obj, True or False)
            group = list(ChatGroup.objects.get_or_create(group_name = requested_group)) 
            group = group[0]
            
            self.group_name = group.group_name
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.group_name ,
                self.channel_name
            )     
            user = self.scope['user']
            self.accept() #this is needed for sending both ok or force disconnect messages
            if user.is_authenticated: 
                group.connect_user(self.scope['user'])
            else:
                self.force_disconnect()
            
        except Exception as e:
            print("############# Exception at consumers.connect ", str(e))
            self.accept()
            self.force_disconnect()
            
    def disconnect(self, close_code):
        # Leave room group
        group = get_object_or_404(ChatGroup, group_name = self.group_name)    
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        group.disconnect_user(self.scope['user'])

    # Receive message from WebSocket, then decide what to do depending on incoming command
    def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']
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


class CheckUnreadMessages(WebsocketConsumer):
    '''
    This class communicates with frontpages/layout.html  script at the bottom
    '''
    def connect(self):
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ tring to fetch unread messages for ",self.scope['user'] )
        
        self.user = self.scope['user']
        self.accept()
        
            
        
        

    def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']
        if not self.user.is_authenticated:
            self.send(text_data = json.dumps({'unread_messages':'AnonymousUser'}))
        else:
            unread_messages = get_unread_grouped_messages(self.user)
            self.send_message(unread_messages)
    
    def send_message(self, message):
        num = ChatMessage.count_unread_message(self.user)
        self.send(text_data = json.dumps({'num':num, 'unread_messages':message}))    


    def disconnect(self, close_code):
        # Leave room group
        print("Closed connection because anonymus user", close_code )
